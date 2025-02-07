import json
import socket 
from dotenv import load_dotenv
import os
import readline # Need to import readline to allow inputs to accept string with length > 1048
import sys
sys.path.append('../')
from helpers.socket_io import read_socket, write_socket

load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

if __name__ == "__main__":
    # Establish connection to server 
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((HOST, PORT))
    
    try:
        while True:
            
            # Steve Attempt
            command = input("Enter command (signup, login, send_chat): ")
            if command == "signup" or command == "login":
                username = input("Enter username: ")
                password = input("Enter password: ")
                msg_data = {"command": command, "username": username, "password": password}
            else: 
                msg = input("Enter message to send: ")
                msg_data = {"command": command, "message": msg}



            # msg = input("Enter message to send: ")
            # # msg_data = {"message": msg, "command": "send_chat"}
            # msg_data = {"message": msg, "command": "signup"}

            sent = write_socket(client_sock, msg_data) 
            data = read_socket(client_sock)
              
            if not data:
                print("Connection closed by server")
                break
            else:
                data = data.decode("utf-8")
                data = json.loads(data)
                print('Received from server:', data["message"])
      
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        client_sock.close()

        
    