from collections import defaultdict
import datetime
import time
from dotenv import load_dotenv
import readline # Need to import readline to allow inputs to accept string with length > 1048
import sys
import grpc
from concurrent import futures
from client_listener import Client_Listener
sys.path.append('../protos')
import server_pb2
import server_pb2_grpc
import client_listener_pb2
import client_listener_pb2_grpc

class Client:
    def __init__(self, server_host, server_port, client_host, username=None):
        self.server_host = server_host
        self.server_port = server_port
        self.client_host = client_host
        
        self.channel = grpc.insecure_channel(f"{server_host}:{server_port}")
        # bind the client and the server
        self.stub = server_pb2_grpc.ServerStub(self.channel)

        self.username = username
    
    def signup(self, username, password):
        ''' 
            Attempts to create a new account with the given username and password. 
        '''

        request = {
            "username": username, 
            "password": password,
        }

        request = server_pb2.UserAuthRequest(**request)
        res = self.stub.Signup(request)

        if res.success:
            self.username = username

        return res.success, res.message
    
    def login(self, username, password):
        '''
            Attempts to login with the given username and password.
        '''

        request = {
            "username": username, 
            "password": password
        }

        request = server_pb2.UserAuthRequest(**request)
        response = self.stub.Login(request)

        if response.HasField("success"):
            res = response.success
            self.username = username
            return res.success, res.message, res.unread_message_count
        else:
            res = response.failure
            return res.success, res.message, -1
   
    def list(self, username_pattern):
        '''
            Lists all usernames that match the given regex username pattern.
        '''

        request = {
            "username_pattern": username_pattern
        }
        request = server_pb2.ListUsernamesRequest(**request)
        response = self.stub.ListUsernames(request)

        if response.HasField("success"):
            res = response.success
            return res.success, res.matches
        else:
            res = response.failure
            return res.success, res.message

    def message(self, target_username, message):
        '''
            Sends a message to the target username.
        '''

        request = {
            "sender_username": self.username, 
            "target_username": target_username, 
            "timestamp": int(time.time()),
            "message": message
        }
        request = server_pb2.SendMessageRequest(**request)
        res = self.stub.SendMessage(request)
        return res.success, res.message
    
    def logout(self):
        '''
            Logs out the current user.
        '''

        request = {
            "username": self.username
        }
        request = server_pb2.UserLogoutRequest(**request)
        res = self.stub.Logout(request)

        if res.success:
            self.username = None
            return res.success, res.message
        else:
            return res.success, res.message
    
    def read(self, num_messages):
        '''
            Reads the last num_messages messages from the user's inbox.
        '''

        request = {
            "username": self.username,
            "num_messages": num_messages
        }
        request = server_pb2.ReadMessagesRequest(**request)
        response = self.stub.ReadMessages(request)

        if response.HasField("success"):

            # Format messages for display
            res = response.success
            messages = []
            for message in res.messages:
                dt = datetime.datetime.fromtimestamp(message.timestamp)
                readable_time = dt.strftime("%m-%d-%Y, %I:%M %p")
                messages.append(f"{message.sender} at ({readable_time}): {message.message}")
            return res.success, messages
        else:
            res = response.failure
            return res.success, res.message
        

    def delete_account(self):
        '''
            Deletes the current user's account.
        '''

        request = {
            "username": self.username
            }
        request = server_pb2.DeleteAccountRequest(**request)
        res = self.stub.DeleteAccount(request)

        if res.success:
            self.username = None
            return res.success, res.message
        else:
            return res.success, res.message
        
    def fetch_sent_messages(self):
        '''
            Fetches all messages that the current user has sent that have not 
            yet been read by the recipient.
        '''

        request = {
            "username": self.username
        }
        request = server_pb2.FetchSentMessagesRequest(**request)
        response = self.stub.FetchSentMessages(request)
        
        if response.HasField("success"):
            res = response.success
            sent_messages = defaultdict(list)

            for msg in res.sent_messages:
                for message in msg.messages:
                    sent_messages[msg.target_username].append({
                        "message_id": message.message_id,
                        "message": message.message,
                        "timestamp": message.timestamp
                    })
            return res.success, sent_messages
        else:
            res = response.failure
            return res.success, res.message

    
    def delete_message(self, message_id): 
        '''
            Deletes the message with the given message_id.
        '''

        if not self.username:
            return False, "You are not logged in! Delete message unsuccessful"
        request = {"sender_username": self.username, "message_id": message_id}
        request = server_pb2.DeleteMessageRequest(**request)
        res = self.stub.DeleteMessage(request)
        return res.success, res.message

    
    def _register_listening_server(self, port):
        '''
            Registers the client's listener with the server so the server knows
            where to forward messages that must be delivered immediately to the client.
        '''

        request = {
            "username": self.username,
            "host": self.client_host,
            "port": port
        }
        register_listener_request = server_pb2.RegisterClientRequest(**request)
        res = self.stub.RegisterClient(register_listener_request)
        print(res)
        return

    
    def listen_for_messages(self, update_ui_callback):
        '''
            Create server on the client that listens for messages from the server
            that must be delivered immediately
        '''

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        client_listener_pb2_grpc.add_Client_ListenerServicer_to_server(
            Client_Listener(update_ui_callback), 
            server
        )
        address = f"{self.client_host}:{0}"
        port = server.add_insecure_port(address)
        server.start()
        print(f"Running server on address")
        print(f"Bound to port: {port}")

        # Register the client's listener with the server
        self._register_listening_server(port)

        server.wait_for_termination()

        