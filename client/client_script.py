import datetime
import json
import selectors
import threading
import time
import socket
import types 
from dotenv import load_dotenv
import os
import readline # Need to import readline to allow inputs to accept string with length > 1048
from client_socket import attempt_login, attempt_signup
import sys
sys.path.append('../')
from helpers.socket_io import read_socket, write_socket

load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

class Client:
    def __init__(self, host, port, username=None):
        self.host = host
        self.port = port
        self.sock = None
        self.username = username
        self.sel = selectors.DefaultSelector()
        self.lsock = None
    
    def signup(self):
        print("Selected: Signup")
        username = input("Enter username: ")
        password = input("Enter password: ")
        msg_data = {"command": "signup", "username": username, "password": password}

        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            print(f"Signup Failed. Please try again: Server side error while attempting login. Please try again!")
        
        data = data.decode("utf-8")
        data = json.loads(data)
        if data["success"]:
            print("Successfully signed up!")
            self.username = username
        else:
            print(f"Signup Failed. Please try again: {data['message']}")
    
    def login(self):
        print("Selected: Login")
        username = input("Enter username: ")
        password = input("Enter password: ")
        msg_data = {"command": "login", "username": username, "password": password}

        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)
        if not data:
            print(f"Login Failed. Please try again: Server side error while attempting login. Please try again!")
        
        data = data.decode("utf-8")
        data = json.loads(data)
        if data["success"]:
            print("Successfully logged in!")
            self.username = username
        else:
            print(f"Login Failed. Please try again: {data['message']}")
   
    def list(self):
        try:
            print("Selected: List")
            username_pattern = input("Enter username regular expression: ")
            msg_data = {"command": "list", "username_pattern": username_pattern}
            sent = write_socket(self.sock, msg_data)
            data = read_socket(self.sock)

            if not data:
                print("Server side error while attempting to list accounts. Please try again!")
                return

            data = data.decode("utf-8")
            data = json.loads(data)
            print(f"Accounts matching pattern {username_pattern}: ")
            for username in data["matches"]:
                print(f"{username}")
            print("\n")
        except Exception as e:
            print(f"Error listing accounts: {e}") 

    def message(self):
        try:
            print("Selected: Message")
            target_username = input("Enter username to message: ")
            message = input("Enter message: ")

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
                print("Server side error while attempting to send message. Please try again!")
                return

            data = data.decode("utf-8")
            data = json.loads(data)
            if data["success"]:
                print(f"Message sent successfully to {target_username}")
            else:
                print(f"Failed to send message: {data['message']}")
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def logout(self):
        try:
            print("Logging Out...")
            if not self.username:
                print("You are not logged in! Logout unsuccessful")
                return
            
            msg_data = {"command": "logout", "username": self.username}
            sent = write_socket(self.sock, msg_data)
            data = read_socket(self.sock)

            if not data:
                print("Server side error while attempting to logout. Please try again!")
                return

            data = data.decode("utf-8")
            data = json.loads(data)
            if data["success"]:
                print(f"Successfully logged out of {self.username}")
                self.username = None
            else:
                print(f"Failed to logout: {data['message']}")
        except Exception as e:
            print(f"Error logging out: {e}")
    
    def read(self):
        try:
            print("Selected: Read")
            num_messages = input("Enter number of messages to read: ")

            msg_data = {"command": "read", "username": self.username, "num_messages": num_messages}
            sent = write_socket(self.sock, msg_data)
            data = read_socket(self.sock)

            if not data:
                print("Server side error while attempting to read messages. Please try again!")
                return

            data = data.decode("utf-8")
            data = json.loads(data)
            if data["success"]:
                for message in data["messages"]:
                    dt = datetime.datetime.fromtimestamp(message["timestamp"])
                    readable_time = dt.strftime("%m-%d-%Y, %I:%M %p")

                    print(f"{message['sender']} at {readable_time}:")
                    print(f"{message['message']}")
                print("\n")
            else:
                print(f"Failed to read messages: {data['message']}")
        except Exception as e:
            print(f"Error reading messages: {e}")

    def delete_account(self):
        try:
            print("Selected: Delete Account")
            if not self.username:
                print("You are not logged in! Delete account unsuccessful")
                return

            msg_data = {"command": "delete_account", "username": self.username}
            sent = write_socket(self.sock, msg_data)
            data = read_socket(self.sock)

            if not data:
                print("Server side error while attempting to delete account. Please try again!")
                return

            data = data.decode("utf-8")
            data = json.loads(data)
            if data["success"]:
                print(f"Successfully deleted account {self.username}")
                self.username = None
            else:
                print(f"Failed to delete account: {data['message']}")
        except Exception as e:
            print(f"Error deleting account: {e}")
    
    def delete_message(self):
        try: 
            print("Selected: Delete Message")
            if not self.username:
                print("You are not logged in! Delete message unsuccessful")
                return
            
            sent_db_pathname = os.path.join("..", "db", "sent_messages", f"{self.username}.json")
            if not os.path.exists(sent_db_pathname):
                print("No sent messages found.")
                return
            
            with open(sent_db_pathname, "r") as f:
                sent_messages = json.load(f)

            print("Sent Messages: ")
            for recipient, messages in sent_messages.items():
                for message in messages: 
                    print(recipient)
                    print(message)
                    print(message['message_id'])
                    print(f"To {recipient}: {message['message']} (ID: {message['message_id']})")
            
            message_id = input("Enter message ID to delete: ")
            msg_data = {"command": "delete_message", "username": self.username, "message_id": message_id}
            sent = write_socket(self.sock, msg_data)
            data = read_socket(self.sock)

            if not data:
                print("Server side error while attempting to delete message. Please try again!")
                return
            
            data = data.decode("utf-8")
            data = json.loads(data)
            if data["success"]:
                print(f"Successfully deleted message {message_id}")
            else:
                print(f"Failed to delete message: {data['message']}")
        except Exception as e:
            print(f"Error deleting message: {e}")
    
    def _register_lsock(self):
        '''
            Register socket to listen for messages from the server that must be
            delivered immediately. 
        '''
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.host, 0))
        self.lsock.listen()
        print(f"Listening for messages on {self.lsock.getsockname()}")
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

        # Register listening socket with server
        msg_data = {
            "command": "register", 
            "username": self.username, 
            "host": self.host, 
            "port": self.lsock.getsockname()[1]
        }
        sent = write_socket(self.sock, msg_data)
        data = read_socket(self.sock)

        if not data:
            print(f"Server side error while attempting to register listening socket for messages. Please try again!")
        
        data = data.decode("utf-8")
        data = json.loads(data)

        if not data["success"]:
            print(f"Failed to register for messages: {data['message']}")
            sys.exit(1)
        print("Successfully registered for online messages on server")

    
    def listen_for_messages(self):
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
                        print(f"REMOVE THIS PRINT LATER: Closing connection to {sock.getpeername()}")
                        self.sel.unregister(sock)
                        sock.close()

                    # Server sent message                    
                    else:
                        data = recv_data.decode("utf-8")
                        data = json.loads(data)
                        print(f"\nNew message from {data['sender']}: {data['message']}")

if __name__ == "__main__":
    client = Client(HOST, PORT)
    try:
        # Establish connection to server 
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((HOST, PORT))
        client.sock = client_sock

    except Exception as e:
        print("Error connecting to server:", e)
        sys.exit(1)
    

    try:
        while True: 
            if client.username is None:
                print("Welcome! To login, type '\login'. To signup, type '\signup'")
                command = input("Enter command: ")

                match command:
                    case "\login":
                        client.login()
                    case "\signup":
                        client.signup()
                    case _:
                        print("Invalid command. Please try again")
                print("\n")
            else: 
            # Start background thread to listen for messages
                messages_thread = threading.Thread(target=client.listen_for_messages, daemon=True)
                messages_thread.start()

                # Login successful, proceeding to chat
                while client.username:
                    commands = ["\list", "\message", "\logout", '\delete_message', "\\read", "\delete_account"]
                    print(f"Welcome {client.username}! Please choose a command:")
                    for command in commands:
                        print(command)

                    command = input("Enter command: ")

                    match command:
                        case "\list":
                            client.list()
                        case "\message":
                            client.message()
                        case "\logout":
                            client.logout()
                            break
                        case "\delete_message":
                            client.delete_message()
                        case "\\read":
                            client.read()
                        case "\delete_account":
                            client.delete_acc()
                            break
                        case _:
                            print("Invalid command. Please try again")
                
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        if client.username:
            client.logout()

        client.sock.close()

        
    