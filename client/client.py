import datetime
import selectors
import time
import socket
import types 
from dotenv import load_dotenv
import os
import readline # Need to import readline to allow inputs to accept string with length > 1048
import sys
import grpc
from concurrent import futures
from client_listener import Client_Listener
sys.path.append('../')
import server_pb2
import server_pb2_grpc
import client_listener_pb2
import client_listener_pb2_grpc
from helpers.socket_io import read_socket, write_socket
from helpers.serialization import deserialize

class Client:
    def __init__(self, server_host, server_port, client_host, username=None):
        self.server_host = server_host
        self.server_port = server_port
        self.client_host = client_host
        
        self.channel = grpc.insecure_channel(f"{server_host}:{server_port}")
        # bind the client and the server
        self.stub = server_pb2_grpc.ServerStub(self.channel)



        self.sock = None
        self.username = username
        self.sel = selectors.DefaultSelector()
        self.lsock = None
    
    # def connect(self):
    #     try:
    #         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         self.sock.connect((self.server_host, self.server_port))
    #     except Exception as e:
    #         print("Error connecting to server:", e)
    #         sys.exit(1)
    
    def signup(self, username, password):
        request = {
            "username": username, 
            "password": password,
            "host": self.client_host,
            "port": 5000    #TODO: FIX THIS PORT
        }
        signup_request = server_pb2.UserAuthRequest(**request)
        print(signup_request)
        res = self.stub.Signup(signup_request)
        print(res, res.success, res.message)
        if res.success:
            self.username = username

        return res.success, res.message
    
    def login(self, username, password):
        request = {
            "username": username, 
            "password": password,
            "host": self.client_host,
            "port": 5000    #TODO: FIX THIS PORT
        }

        login_request = server_pb2.UserAuthRequest(**request)
        response = self.stub.Login(login_request)
        print(response, response.login_response, response.login_failure)

        if response.HasField("login_response"):
            res = response.login_response
            print(res)
            self.username = username
            return res.success, res.message, res.unread_message_count
        else:
            res = response.login_failure
            print("failed:", res)
            return res.success, res.message, -1
   
    def list(self, username_pattern):
        request = {
            "username_pattern": username_pattern
        }
        list_request = server_pb2.ListUsernamesRequest(**request)
        response = self.stub.ListUsernames(list_request)

        if response.HasField("usernames"):
            res = response.usernames
            return res.success, res.matches
        else:
            res = response.failure
            return res.success, res.message

        msg_data = {"command": "list", "username": self.username, "username_pattern": username_pattern}
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            return False, "Server side error while attempting to list users. Please try again!" 
               
        data = deserialize(data)
        if data["success"]:
            return True, data["matches"]
        else:
            return False, data["message"]

    def message(self, target_username, message):
        request = {
            "sender_username": self.username, 
            "target_username": target_username, 
            "timestamp": int(time.time()),
            "message": message
        }
        message_request = server_pb2.SendMessageRequest(**request)
        res = self.stub.SendMessage(message_request)
        return res.success, res.message
        
        
        
        
        msg_data = {
            "command": "message", 
            "sender_username": self.username,
            "target_username": target_username, 
            "message": message,
            "timestamp": int(time.time())
        }
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            return False, "Server side error while attempting to send message. Please try again!"     
          
        data = deserialize(data)
        if data["success"]:
            return True, f"Message sent successfully to {target_username}!"
        else:
            return False, data["message"]
    
    def logout(self):        
        request = {
            "username": self.username
        }
        logout_request = server_pb2.UserLogoutRequest(**request)
        res = self.stub.Logout(logout_request)
        print(res)
        if res.success:
            self.username = None
            return res.success, res.message
        else:
            return res.success, res.message
        
        if not self.username:
            return False, "You are not logged in! Logout unsuccessful"
        msg_data = {"command": "logout", "username": self.username}
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            return False, "Server side error while attempting to logout. Please try again!"  
              
        data = deserialize(data)
        if data["success"]:
            self.username = None
            return True, "Successfully logged out!"
        else:
            return False, data["message"]
    
    def read(self, num_messages):
        request = {
            "username": self.username,
            "num_messages": num_messages
        }
        read_request = server_pb2.ReadMessagesRequest(**request)
        response = self.stub.ReadMessages(read_request)

        if response.HasField("read_messages"):
            res = response.read_messages
            messages = []
            for message in res.messages:
                dt = datetime.datetime.fromtimestamp(message.timestamp)
                readable_time = dt.strftime("%m-%d-%Y, %I:%M %p")
                messages.append(f"{message.sender} at ({readable_time}): {message.message}")
            return res.success, messages
        else:
            res = response.failure
            return res.success, res.message
        
        msg_data = {"command": "read", "username": self.username, "num_messages": num_messages}
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            return False, "Server side error while attempting to read messages. Please try again!"
        
        data = deserialize(data)
        if data["success"]:
            messages = []
            for message in data["messages"]:
                dt = datetime.datetime.fromtimestamp(message["timestamp"])
                readable_time = dt.strftime("%m-%d-%Y, %I:%M %p")
                messages.append(f"{message['sender']} at ({readable_time}): {message['message']}")
            return True, messages
        else:
            return False, data["message"]

    def delete_account(self):
        request = {
            "username": self.username
            }
        delete_account_request = server_pb2.DeleteAccountRequest(**request)
        res = self.stub.DeleteAccount(delete_account_request)

        if res.success:
            self.username = None
            return res.success, res.message
        else:
            return res.success, res.message
        
        if not self.username:
            return False, "You are not logged in! Delete account unsuccessful"
        msg_data = {"command": "delete_account", "username": self.username}
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            return False, "Server side error while attempting to delete account. Please try again!"
        
        # data = json.loads(data.decode("utf-8"))
        data = deserialize(data)
        if data["success"]:
            self.username = None
            return True, "Successfully deleted account!"
        else:
            return False, data["message"]
        
    def fetch_sent_messages(self):
        request = {
            "username": self.username
        }
        fetch_sent_messages_request = server_pb2.FetchSentMessagesRequest(**request)
        response = self.stub.FetchSentMessages(fetch_sent_messages_request)
        
        if response.HasField("sent_messages"):
            res = response.sent_messages
            sent_messages = {}
            for msg in response.messages:
                if msg.recipient not in sent_messages:
                    sent_messages[msg.recipient] = []
                sent_messages[msg.recipient].append({
                    "message_id": msg.message_id,
                    "message": msg.message,
                    "timestamp": msg.timestamp
                })
            return res.success, sent_messages
        else:
            res = response.failure
            return res.success, res.message
        
        
        if not self.username:
            return False, "You are not logged in! Fetch sent messages unsuccessful"
        msg_data = {"command": "fetch_sent_messages", "username": self.username}
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            return False, "Server side error while attempting to fetch sent messages. Please try again!"
    
        data = deserialize(data)
        if data["success"]:
            return True, data["sent_messages"]
        else:
            return False, data["message"]
    
    def delete_message(self, message_id): 
        if not self.username:
            return False, "You are not logged in! Delete message unsuccessful"
        msg_data = {"command": "delete_message", "username": self.username, "message_id": message_id}
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)

        if not data:
            return False, "Server side error while attempting to delete message. Please try again!"
        
        data = deserialize(data)
        if data["success"]:
            return True, f"Successfully deleted message {message_id}!"
        else:
            return False, data["message"]
    
    def _register_listening_server(self):
        '''
            Create gRPC server on the client side that listens for messages from
            the server that must be delivered immediately
        '''
        pass

    def _register_lsock(self):
        '''
            Register socket to listen for messages from the server that must be
            delivered immediately. 
        '''
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.client_host, 0))
        self.lsock.listen()
        print(f"Listening for messages on {self.lsock.getsockname()}")
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

        # Register listening socket with server
        msg_data = {
            "command": "register", 
            "username": self.username, 
            "host": self.client_host, 
            "port": self.lsock.getsockname()[1]
        }
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)

        if not data:
            print(f"Server side error while attempting to register listening socket for messages. Please try again!")
            sys.exit(1)
        
        data = deserialize(data)

        if not data["success"]:
            print(f"Failed to register for messages: {data['message']}")
            sys.exit(1)
        print("Successfully registered for online messages on server")

    
    def listen_for_messages(self, update_ui_callback):
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

        # Register Client Listener with Server
        request = {
            "username": self.username,
            "host": self.client_host,
            "port": port
        }
        register_listener_request = server_pb2.RegisterClientRequest(**request)
        res = self.stub.RegisterClient(register_listener_request)
        print(res)

        server.wait_for_termination()

        


        # self._register_lsock()

        # while True:
        #     events = self.sel.select(timeout=None)
        #     for key, mask in events:
        #         sock = key.fileobj

        #         # Accept connection from server
        #         if key.data is None:
        #             conn, addr = self.lsock.accept()
        #             print(f"Accepted connection from {addr}")
        #             conn.setblocking(False)
        #             data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        #             events = selectors.EVENT_READ | selectors.EVENT_WRITE
        #             self.sel.register(conn, events, data=data)
        #             continue
                
        #         # Receive message from server 
        #         if mask & selectors.EVENT_READ:
        #             recv_data = read_socket(sock)

        #             # Server closed connection
        #             if not recv_data:
        #                 print(f"In Background Thread: Closing connection to {sock.getpeername()}")
        #                 self.sel.unregister(sock)
        #                 sock.close()

        #             # Server sent message                    
        #             else:
        #                 data = deserialize(recv_data)
        #                 message = f"\nNew message from {data['sender']}: {data['message']}"
        #                 print(message)
                        # update_ui_callback(message)
