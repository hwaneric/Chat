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
            # message = input("Enter message to send: ")
            # client_sock.send(message.encode('utf-8'))

            message = input("Enter message to send: ")
            sent = write_socket(client_sock, message)
            # message_length = len(message)
            # message_length_bytes = message_length.to_bytes(4, byteorder='big')
            # full_message = message_length_bytes + message.encode('utf-8')
            # client_sock.send(full_message)
            data = read_socket(client_sock)
            # data = b''
            # while True:
            #     part = client_sock.recv(1024)
            #     data += part
            #     if len(part) < 1024:
            #         break
            if not data:
                print("Connection closed by server")
                break
            else:
                print('Received from server:', data.decode('utf-8'))
      
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        client_sock.close()

        
    