# def service_connection():
#   pass
import json
import selectors

import sys
sys.path.append('../')
from helpers.socket_io import read_socket, write_socket
from account_management import check_if_online, create_account, list_accounts, login, logout, send_offline_message

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
                case "send_chat":
                    return_msg = decoded_data["message"] + " TESTTTT"
                    return_data = {"message": return_msg}
                    sent = write_socket(sock, return_data)
                    print(f"Sending {return_data} to {data.addr}")
                    data.outb = b''     # TODO: This is a hack to get it to work for now. This may be problematic if not all of the message is sent at once.
                    
                case "signup":
                    username = decoded_data["username"]
                    password = decoded_data["password"]
                    return_data = create_account(username, password)
                    sent = write_socket(sock, return_data)
                    print(f"Sending {return_data} to {data.addr}")
                    data.outb = b''
#                   
                case "login":
                    username = decoded_data["username"]
                    password = decoded_data["password"]
                    return_data = login(username, password)
                    sent = write_socket(sock, return_data)
                    print(f"Sending {return_data} to {data.addr}")
                    data.outb = b''
                
                case "logout":
                    username = decoded_data["username"]
                    return_data = logout(username)
                    sent = write_socket(sock, return_data)
                    print(f"Sending {return_data} to {data.addr}")
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

                    message = decoded_data["message"]
                    return_data = send_offline_message(target_username, message, timestamp)
                    
                    sent = write_socket(sock, return_data)
                    print(f"Sending {return_data} to {data.addr}")
                    data.outb = b''




                case _:
                    unrecognized_command_message = "Unrecognized command. Please try again!"

                    return_data = {"message": unrecognized_command_message}

                    sent = write_socket(sock, return_data)
                    print(f"Sending {return_data} to {data.addr}")
                    data.outb = b''
           
