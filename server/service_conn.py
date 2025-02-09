# def service_connection():
#   pass
import json
import selectors

import socket
import sys
sys.path.append('../')
from helpers.socket_io import read_socket, write_socket
from account_management import check_if_online, create_account, list_accounts, login, logout, read_messages, send_offline_message

socket_map = {}

def service_connection(sel, key, mask):
    sock = key.fileobj
    data = key.data
    
    if mask & selectors.EVENT_READ:
        recv_data = read_socket(sock)

        if not recv_data:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
        else:
            data.outb += recv_data

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            decoded_data = data.outb.decode("utf-8").strip()
            print("raw data:", data.outb, "decoded_data:", decoded_data)
            decoded_data = json.loads(decoded_data)
          
            match decoded_data["command"]:
                case "signup":
                    username = decoded_data["username"]
                    password = decoded_data["password"]
                    host, port = data.addr
                    return_data = create_account(username, password, host, port)

                    # socket_map[username] = sock
                    sent = write_socket(sock, return_data)
                    print(f"Sending {return_data} to {data.addr}")
                    print(f"Socket map: {socket_map}")
                    data.outb = b''
                   
                case "login":
                    username = decoded_data["username"]
                    password = decoded_data["password"]
                    host, port = data.addr

                    return_data = login(username, password, host, port)
                    sent = write_socket(sock, return_data)
                    print(f"Sending {return_data} to {data.addr}")
                    data.outb = b''
                
                case "logout":
                    username = decoded_data["username"]
                    return_data = logout(username)
                    sent = write_socket(sock, return_data)
                    print(f"Sending {return_data} to {data.addr}")
                    if username in socket_map:
                        del socket_map[username]
                    print(f"Socket map: {socket_map}")
                    data.outb = b''

                case "list":
                    username_pattern = decoded_data["username_pattern"]
                    return_data = list_accounts(username_pattern)
                    sent = write_socket(sock, return_data)
                    print(f"Sending {return_data} to {data.addr}")
                    data.outb = b''

                case "message":
                    target_username = decoded_data["target_username"]
                    message = decoded_data["message"]
                    timestamp = int(decoded_data["timestamp"])  # Seconds since epoch
                    sender_username = decoded_data["sender_username"]
                    message = decoded_data["message"]

                    target_logged_in = check_if_online(target_username)

                    if target_logged_in and target_username in socket_map:
                        target_socket = socket_map[target_username]
                        return_data_to_recipient = {
                            "success": True, 
                            "message": message, 
                            "sender": sender_username
                        }
                        sent = write_socket(target_socket, return_data_to_recipient)

                        return_data_to_sender = {
                            "success": True,
                            "message": f"Message sent successfully to {target_username}"
                        }
                        sent = write_socket(sock, return_data_to_sender)
                        data.outb = b''

                    else:
                        return_data = send_offline_message(target_username, sender_username, message, timestamp)
                        sent = write_socket(sock, return_data)
                        print(f"Sending {return_data} to {data.addr}")
                        data.outb = b''

                case "register":
                    username = decoded_data["username"]
                    host = decoded_data["host"]
                    port = decoded_data["port"]

                    msg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    msg_socket.connect((host, port))
                    socket_map[username] = msg_socket
                    return_data = {"message": "Registered successfully", "success": True}
                    sent = write_socket(sock, return_data)
                    data.outb = b''
                
                case "read":
                    username = decoded_data["username"]
                    num_messages = int(decoded_data["num_messages"])
                    return_data = read_messages(username, num_messages)
                    sent = write_socket(sock, return_data)
                    data.outb = b''



                    


                case _:
                    unrecognized_command_message = "Unrecognized command. Please try again!"

                    return_data = {"message": unrecognized_command_message}

                    sent = write_socket(sock, return_data)
                    print(f"Sending {return_data} to {data.addr}")
                    data.outb = b''
           
