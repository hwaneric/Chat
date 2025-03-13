from concurrent import futures
import time
import grpc
import sys
sys.path.append('../protos')
import server_pb2 
import server_pb2_grpc
import client_listener_pb2
import client_listener_pb2_grpc
from account_management import check_if_online, create_account, fetch_sent_messages, list_accounts, login, logout, logout_all_users, read_messages, send_offline_message, delete_account, delete_message
import threading

from dotenv import load_dotenv
import os
load_dotenv()
HOST = os.getenv("SERVER_HOST")
PORT = int(os.getenv("SERVER_PORT"))

class Server(server_pb2_grpc.ServerServicer):
    def __init__(self, id, host, port, db_path=None):
        # Map of username to client stub for sending messages to clients that must be delivered immediately
        self.stub_map = {} 

        # Map of Stubs to Peer Servers 
        self.server_stubs = {}

        self.id = id
        self.is_leader = False
        self.db_path = None

        self.host = host
        self.port = port

        if db_path:
            if os.path.exists(db_path):
                self.db_path = db_path
            else:
                print("Database does not exist. Using default instead.")
        else:
            self.db_path = get_db_pathname(id)
        print(self.db_path)
    
    def Signup(self, request, context):
        username = request.username
        password = request.password

        print(f"Received signup request from {username}")
        res = create_account(username, password, self.db_path)

        return server_pb2.StandardServerResponse(**res)
        
    def Login(self, request, context):
        username = request.username
        password = request.password
        
        print(f"Received login request from {username}")
        res = login(username, password, self.db_path)

        server_response = server_pb2.UserLoginResponse() 
        if res["success"]:
            print(res)
            user_login_success = server_pb2.UserLoginSuccess(**res)  # create UserLoginSuccess
            server_response.success.CopyFrom(user_login_success)  # assign to login_response
        else:
            print(res)
            standard_server_response = server_pb2.StandardServerResponse(**res)  # create StandardServerResponse
            server_response.failure.CopyFrom(standard_server_response)  # assign to login_response
        return server_response
      
    def Logout(self, request, context):
        username = request.username
        print(f"Received logout request from {username}")
        res = logout(username, self.db_path)

        if username in self.stub_map:
            del self.stub_map[username]

        return server_pb2.StandardServerResponse(**res)

    def ListUsernames(self, request, context):
        username_pattern = request.username_pattern
        print("Received list accounts request")
        res = list_accounts(username_pattern, self.db_path)
        
        server_response = server_pb2.ListUsernamesResponse()
        if res["success"]:
            usernames = server_pb2.ListUsernames(
                success = res["success"],
                message = res["message"],
                matches = res["matches"]
            )
            server_response.success.CopyFrom(usernames)
        else:
            failure = server_pb2.StandardServerResponse(
                success=res["success"],
                message=res["message"]
            )
            server_response.failure.CopyFrom(failure)
        
        return server_response
    
    def SendMessage(self, request, context):
        sender = request.sender_username
        target = request.target_username
        message = request.message
        timestamp = request.timestamp
        print(f"Received message from {sender} to {target}")

        target_logged_in = check_if_online(target, self.db_path)
        if target_logged_in and target in self.stub_map:
            print("Target is online, sending online message")

            res = {"success": True, "message": message, "sender": sender}
            online_message = client_listener_pb2.OnlineMessage(**res)

            stub = self.stub_map[target]
            stub.SendOnlineMessage(online_message)

            return server_pb2.StandardServerResponse(success=True, message="Message sent successfully")

        else:
            res = send_offline_message(target, sender, message, timestamp, self.db_path)
            return server_pb2.StandardServerResponse(**res)
    
    def RegisterClient(self, request, context):
        '''
            Registers a client stub to the server for sending messages to the client
        '''

        username = request.username
        host = request.host
        port = request.port

        channel = grpc.insecure_channel(f"{host}:{port}")
        stub = client_listener_pb2_grpc.Client_ListenerStub(channel)
        print(f"Received register client request from {username}")

        self.stub_map[username] = stub
        return server_pb2.StandardServerResponse(success=True, message= "Registered successfully")

    def ReadMessages(self, request, context):
        username = request.username
        num_messages = request.num_messages
        print(f"Received read messages request from {username}")
        res = read_messages(username, num_messages, self.db_path)

        server_response = server_pb2.ReadMessageResponse()
        if res["success"]:
            read_message = server_pb2.ReadMessage(
                success=res["success"],
                message=res["message"],
                messages=res["messages"]
            )
            server_response.success.CopyFrom(read_message)
        else:
            failure = server_pb2.StandardServerResponse(
                success=res["success"],
                message=res["message"]
            )
            server_response.failure.CopyFrom(failure)

        return server_response

    def DeleteAccount(self, request, context):
        username = request.username
        print(f"Received delete account request from {username}")
        res = delete_account(username, self.db_path)

        if username in self.stub_map:
            del self.stub_map[username]
        
        return server_pb2.StandardServerResponse(**res)

    def DeleteMessage(self, request, context):
        username = request.sender_username
        message_id = request.message_id
        print(f"Received delete message request from {username}")

        res = delete_message(username, message_id, self.db_path)
        return server_pb2.StandardServerResponse(**res)
    
    def FetchSentMessages(self, request, context):
        username = request.username
        print(f"Received fetch sent messages request from {username}")
        res = fetch_sent_messages(username, self.db_path)

        response = server_pb2.FetchSentMessagesResponse()
        if res["success"]:
            response_body = server_pb2.FetchedSentMessages(
                success=res["success"],
                message=res["message"],
            )

            # Add sent messages to server response
            for target_username, messages in res["sent_messages"].items():
                sent_messages = server_pb2.SentMessages(
                    target_username=target_username
                )

                for message in messages:
                    unread_message = server_pb2.UnreadMessage(**message)
                    sent_messages.messages.append(unread_message)
                    
                response_body.sent_messages.append(sent_messages)


            response.success.CopyFrom(response_body)
        else:
            failure = server_pb2.StandardServerResponse(
                success=res["success"],
                message=res["message"]
            )
            response.failure.CopyFrom(failure)
        return response

    def cleanup(self):
        '''
            Cleans up the server by logging out all users
        '''
        print("Cleaning up server")
        logout_all_users(self.db_path)
        print("Logged out all users")
        print("Server cleanup complete")
    
    


def serve(server_object):
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_pb2_grpc.add_ServerServicer_to_server(server_object, server)
        address = f"{server_object.host}:{server_object.port}"
        server.add_insecure_port(address)
        server.start()
        print(f"Running server on host: {server_object.host} and port: {server_object.port}")
        server.wait_for_termination()

    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
        logout_all_users(server_object.db_path)

def connect(server_object):
    '''
        Connects to other servers in the cluster
    '''
    print("Attempting to Connect to other servers")

    # Create a channel to connect to other servers
    for i in range(3):
        if i == server_object.id:
            continue

        host = os.getenv(f"SERVER_HOST_{i}")
        port = int(os.getenv(f"SERVER_PORT_{i}"))

        MAX_RETRIES = 20
        retry_delay = 2  # seconds

        # Attempt to connect to the server of client {id}
        for attempt in range(MAX_RETRIES):
            try:
                channel = grpc.insecure_channel(f"{host}:{port}")
                grpc.channel_ready_future(channel).result(timeout=retry_delay)
                # channel = grpc.insecure_channel(f"{host}:{port}")
                stub = server_pb2_grpc.ServerStub(channel)
                server_object.server_stubs[i] = stub
                    
            except grpc.FutureTimeoutError:
                # Connection Attempt Timed Out
                if attempt == MAX_RETRIES - 1:
                    print(f"Failed to connect to server {i} after {MAX_RETRIES} attempts.")
                    break

                time.sleep(retry_delay)

        print(f"Connected to server {i}")
    
    print("Connected to all servers")
    
        

def initialize(id, db_path):
    print("host and port", f"SERVER_HOST_{id}", f"SERVER_PORT_{id}")
    host, port = os.getenv(f"SERVER_HOST_{id}"), int(os.getenv(f"SERVER_PORT_{id}"))
    server_object = Server(id, host, port, db_path)

    # Set Server 0 As Leader
    if id == 0:
        server_object.is_leader = True
        print("Server is leader")
    else:
        print("Server is not leader")

    # Connect to other servers in background thread
    threading.Thread(target=connect, args=(server_object,), daemon=True).start()

    serve(server_object)
    server_object.cleanup()

def get_db_pathname(id):
    print('id', id)
    current_dir = os.path.dirname(__file__)
    base_dir = os.path.dirname(current_dir)
    db_pathname = os.path.join(base_dir, f'db_{id}')

    # db_pathname = os.path.join(base_dir, f'db')

    return db_pathname



if __name__ == '__main__':
    # serve()
    if len(sys.argv) < 2:
        print("Usage: python driver.py <server_id>")
        sys.exit(1)
    
    # Get command line arguments
    server_id = sys.argv[1]
    db_path = None
    if len(sys.argv) == 3:
        db_path = sys.argv[2]

    # Validate Command Line Arguments
    if not server_id.isdigit():
        print("Invalid server ID. Server ID must be an integer.")
        sys.exit(1)

    server_id = int(server_id)
    print("hello", server_id)
    if server_id not in [0, 1, 2]:
        print("Invalid server ID. Please provide 0, 1, or 2.")
        sys.exit(1)

    initialize(server_id, db_path)
