from concurrent import futures
import time
import grpc
import sys
sys.path.append('../')
import server_pb2
import server_pb2_grpc
import client_listener_pb2
import client_listener_pb2_grpc
from account_management import check_if_online, create_account, fetch_sent_messages, list_accounts, login, logout, read_messages, send_offline_message, delete_account, delete_message

from dotenv import load_dotenv
import os
load_dotenv()
HOST = os.getenv("SERVER_HOST")
PORT = int(os.getenv("SERVER_PORT"))

class Server(server_pb2_grpc.ServerServicer):
    def __init__(self):
        self.stub_map = {} 
    
    def Signup(self, request, context):
        username = request.username
        password = request.password
        host = request.host
        port = request.port
        print(f"Received signup request from {username}")
        res = create_account(username, password, host, port)

        return server_pb2.StandardServerResponse(**res)
        
    def Login(self, request, context):
        username = request.username
        password = request.password
        host = request.host
        port = request.port
        print(f"Received login request from {username}")
        res = login(username, password, host, port)

        server_response = server_pb2.UserLoginResponse() 
        if res["success"]:
            print(res)
            user_login_success = server_pb2.UserLoginSuccess(**res)  # create UserLoginSuccess
            server_response.login_response.CopyFrom(user_login_success)  # assign to login_response
        else:
            print(res)
            standard_server_response = server_pb2.StandardServerResponse(**res)  # create StandardServerResponse
            server_response.login_failure.CopyFrom(standard_server_response)  # assign to login_response
        return server_response
      
    def Logout(self, request, context):
        username = request.username
        print(f"Received logout request from {username}")
        res = logout(username)

        if username in self.stub_map:
            del self.stub_map[username]

        return server_pb2.StandardServerResponse(**res)

    def ListUsernames(self, request, context):
        username_pattern = request.username_pattern
        print("Received list accounts request")
        res = list_accounts(username_pattern)
        
        response = server_pb2.ListUsernamesResponse()
        if res["success"]:
            usernames = server_pb2.ListUsernames(
                success=res["success"],
                message=res["message"],
                matches=res["matches"]
            )
            response.usernames.CopyFrom(usernames)
        else:
            failure = server_pb2.StandardServerResponse(
                success=res["success"],
                message=res["message"]
            )
            response.failure.CopyFrom(failure)
        
        return response
    
    def SendMessage(self, request, context):
        sender = request.sender_username
        target = request.target_username
        message = request.message
        timestamp = request.timestamp
        print(f"Received message from {sender} to {target}")
        print(f"Stub Map: {self.stub_map}")

        target_logged_in = check_if_online(target)
        if target_logged_in and target in self.stub_map:
            print("Target is online, sending online message")

            stub = self.stub_map[target]
            res = {"success": True, "message": message, "sender": sender}
            online_message = client_listener_pb2.OnlineMessage(**res)
            stub.SendOnlineMessage(online_message)

            # TODO: Handle if online message fails to send
            return server_pb2.StandardServerResponse(success=True, message="Message sent successfully")

        else:
            res = send_offline_message(target, sender, message, timestamp)
            return server_pb2.StandardServerResponse(**res)
    
    def RegisterClient(self, request, context):
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
        res = read_messages(username, num_messages)
        print(res)

        response = server_pb2.ReadMessageResponse()
        if res["success"]:
            read_message = server_pb2.ReadMessage(
                success=res["success"],
                message=res["message"],
                messages=res["messages"]
            )
            response.read_messages.CopyFrom(read_message)
        else:
            failure = server_pb2.StandardServerResponse(
                success=res["success"],
                message=res["message"]
            )
            response.failure.CopyFrom(failure)

        return response

    def DeleteAccount(self, request, context):
        username = request.username
        print(f"Received delete account request from {username}")
        res = delete_account(username)

        if username in self.stub_map:
            del self.stub_map[username]
        
        return server_pb2.StandardServerResponse(**res)

    def DeleteMessage(self, request, context):
        username = request.sender_username
        message_id = request.message_id
        print(f"Received delete message request from {username}")
        res = delete_message(username, message_id)
        return server_pb2.StandardServerResponse(**res)
    
    def FetchSentMessages(self, request, context):
        username = request.username
        print(f"Received fetch sent messages request from {username}")
        res = fetch_sent_messages(username)
        print(res)

        response = server_pb2.FetchSentMessagesResponse()
        if res["success"]:
            sent_message = server_pb2.FetchedSentMessages(
                success=res["success"],
                message=res["message"],
                sent_messages=res["sent_messages"]
            )
            print(sent_message)
            response.sent_messages.CopyFrom(sent_message)
        else:
            failure = server_pb2.StandardServerResponse(
                success=res["success"],
                message=res["message"]
            )
            response.failure.CopyFrom(failure)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_ServerServicer_to_server(Server(), server)
    address = f"{HOST}:{PORT}"
    server.add_insecure_port(address)
    server.start()
    print(f"Running server on host: {HOST} and port: {PORT}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

# import socket
# import selectors
# import types
# from accept_wrapper import accept_wrapper
# from account_management import logout_all_users
# from service_conn import service_connection
# from dotenv import load_dotenv
# import os

# load_dotenv()
# HOST = os.getenv("SERVER_HOST")
# PORT = int(os.getenv("SERVER_PORT"))

# sel = selectors.DefaultSelector()

# if __name__ == "__main__":
#     lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     lsock.bind((HOST, PORT))
#     lsock.listen()
#     print("Listening on", (HOST, PORT))
#     lsock.setblocking(False)
#     sel.register(lsock, selectors.EVENT_READ, data=None)
#     try:
#         while True:
#             events = sel.select(timeout=None)
#             for key, mask in events:
#                 if key.data is None:
#                     accept_wrapper(sel, key.fileobj)
#                 else:
#                     service_connection(sel, key, mask)
#     except KeyboardInterrupt:
#         print("Caught keyboard interrupt, exiting")
#     finally:
#         logout_all_users()
#         sel.close()

