import datetime
import traceback
import json
import selectors
import threading
import time
import socket
import types 
from dotenv import load_dotenv
import os
import readline # Need to import readline to allow inputs to accept string with length > 1048
import sys
sys.path.append('../')
from helpers.socket_io import read_socket, write_socket
from helpers.serialization import deserialize

# load_dotenv()
# HOST = os.getenv("HOST")
# PORT = int(os.getenv("PORT"))

class Client:
    def __init__(self, server_host, server_port, client_host, username=None):
        self.server_host = server_host
        self.server_port = server_port
        self.client_host = client_host
        self.sock = None
        self.username = username
        self.sel = selectors.DefaultSelector()
        self.lsock = None
    
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_host, self.server_port))
        except Exception as e:
            print("Error connecting to server:", e)
            sys.exit(1)
    
    def signup(self, username, password):
        msg_data = {"command": "signup", "username": username, "password": password}
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            return False, "Server side error while attempting signup. Please try again!"        
        
        data = deserialize(data)
        # data = data.decode("utf-8")
        # data = json.loads(data)
        if data["success"]:
            self.username = username
            return True, "Successfully signed up!"
        else:
            return False, data["message"]
    
    def login(self, username, password):
        msg_data = {"command": "login", "username": username, "password": password}
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            return False, "Server side error while attempting login. Please try again!", -1     

        data = deserialize(data)

        if data["success"]:
            self.username = username
            return True, "Successfully logged in!", data["unread_message_count"]
        else:
            return False, data["message"], -1
   
    def list(self, username_pattern):
        msg_data = {"command": "list", "username": self.username, "username_pattern": username_pattern}
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            return False, "Server side error while attempting to list users. Please try again!" 
               
        # data = json.loads(data.decode("utf-8"))
        data = deserialize(data)
        if data["success"]:
            return True, data["matches"]
        else:
            return False, data["message"]

    def message(self, target_username, message):
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
          
        # data = json.loads(data.decode("utf-8"))
        data = deserialize(data)
        if data["success"]:
            return True, f"Message sent successfully to {target_username}!"
        else:
            return False, data["message"]
    
    def logout(self):
        if not self.username:
            return False, "You are not logged in! Logout unsuccessful"
        msg_data = {"command": "logout", "username": self.username}
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            return False, "Server side error while attempting to logout. Please try again!"  
              
        # data = json.loads(data.decode("utf-8"))
        data = deserialize(data)
        if data["success"]:
            self.username = None
            return True, "Successfully logged out!"
        else:
            return False, data["message"]
    
    def read(self, num_messages):
        msg_data = {"command": "read", "username": self.username, "num_messages": num_messages}
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            return False, "Server side error while attempting to read messages. Please try again!"
        
        # data = json.loads(data.decode("utf-8"))
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
        
        # data = data.decode("utf-8")
        # data = json.loads(data)
        data = deserialize(data)

        if not data["success"]:
            print(f"Failed to register for messages: {data['message']}")
            sys.exit(1)
        print("Successfully registered for online messages on server")

    
    def listen_for_messages(self, update_ui_callback):
        self._register_lsock()

        while True:
            events = self.sel.select(timeout=None)
            for key, mask in events:
                sock = key.fileobj

                # Accept connection from server
                if key.data is None:
                    conn, addr = self.lsock.accept()
                    print(f"Accepted connection from {addr}")
                    conn.setblocking(False)
                    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
                    events = selectors.EVENT_READ | selectors.EVENT_WRITE
                    self.sel.register(conn, events, data=data)
                    continue
                
                # Receive message from server 
                if mask & selectors.EVENT_READ:
                    recv_data = read_socket(sock)

                    # Server closed connection
                    if not recv_data:
                        print(f"In Background Thread: Closing connection to {sock.getpeername()}")
                        self.sel.unregister(sock)
                        sock.close()

                    # Server sent message                    
                    else:
                        # data = recv_data.decode("utf-8")
                        # data = json.loads(data)
                        data = deserialize(recv_data)
                        message = f"\nNew message from {data['sender']}: {data['message']}"
                        print(message)
                        update_ui_callback(message)
