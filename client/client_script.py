import json
import time
import socket 
from dotenv import load_dotenv
import os
import readline # Need to import readline to allow inputs to accept string with length > 1048
from user_interface import user_interface_driver
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
            print(f"Signup Failed. Please try again: {data["message"]}")
    
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
            print(f"Login Failed. Please try again: {data["message"]}")
   
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
                print(f"Failed to send message: {data["message"]}")
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
                print(f"Failed to logout: {data["message"]}")
        except Exception as e:
            print(f"Error logging out: {e}")

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

        while client.username is None:
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
        
        # Login successful, proceeding to chat
        while True:
            commands = ["\list", "\message", "\logout"]
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
                case _:
                    print("Invalid command. Please try again")
            # msg = input("Enter message to send: ")
            # msg_data = {"message": msg, "command": "send_chat"}
            # # msg_data = {"message": msg, "command": "signup"}

            # sent = write_socket(client.sock, msg_data) 
            # data = read_socket(client.sock)
            
            # if not data:
            #     print("Connection closed by server, exiting")
            #     break
            # else:
            #     data = data.decode("utf-8")
            #     data = json.loads(data)
            #     print('Received from server:', data["message"])
      
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        if client.username:
            client.logout()

        client.sock.close()

        
    