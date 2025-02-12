import json
import socket 
import curses
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


    

if __name__ == "__main__":
    try:
        # Establish connection to server 
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((HOST, PORT))
    except Exception as e:
        print("Error connecting to server:", e)
        sys.exit(1)
    



    # curses.wrapper(lambda stdscr: user_interface_driver(stdscr, client_sock))


    
    


    # curses.curs_set(0)  # Hide cursor
    # stdscr.keypad(1)  # Enable arrow keys
    # stdscr.clear()
    
    # options = ["Login", "Signup"]
    # current_option = 0
    
    try:
        while True:
            print("Welcome! To login, type '\login'. To signup, type '\signup'")
            command = input("Enter command: ")

            match command:
                case "\login":
                    print("Selected: Login")
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    login_res = attempt_login(client_sock, username, password)
                    if login_res["success"]:
                        print("Successfully logged in!")
                        break
                    else:
                        print(f"Login Failed. Please try again: {login_res["message"]}")
                    
                case "\signup":
                    print("Selected: Signup")
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    signup_res = attempt_signup(client_sock, username, password)

                    if signup_res["success"]:
                        print("Successfully logged in!")
                        break
                    else:
                        print(f"Signup Failed. Please try again: {signup_res["message"]}")

                case _:
                    print("Invalid command. Please try again")
            print("")
                
        # Login successful, proceeding to chat
        while True:
            msg = input("Enter message to send: ")
            msg_data = {"message": msg, "command": "send_chat"}
            # msg_data = {"message": msg, "command": "signup"}

            sent = write_socket(client_sock, msg_data) 
            data = read_socket(client_sock)
            
            if not data:
                print("Connection closed by server, exiting")
                break
            else:
                data = data.decode("utf-8")
                data = json.loads(data)
                print('Received from server:', data["message"])
      
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        client_sock.close()

        
    