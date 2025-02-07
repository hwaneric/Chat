# def service_connection():
#   pass
import json
import selectors

import sys
sys.path.append('../')
from helpers.socket_io import read_socket, write_socket

def service_connection(sel, key, mask):
    sock = key.fileobj
    data = key.data
    
    if mask & selectors.EVENT_READ:
        # data_len = sock.recv(4) # First 4 bytes reserved for data length
        # data_len = int.from_bytes(data_len, byteorder="big")
        # print(f"Data length: {data_len}")

        # # EVENTUALLY INSTEAD OF GETTING THIS ENTIRE LOOP, WE SHOULD JUST SEND THE LENGTH OF THE DATA AND READ IT ALL AT ONCE
        # recv_data = b''
        # recv_data = sock.recv(data_len)
        recv_data = read_socket(sock)

        # while True:
        #     print("Receiving data")
        #     part = sock.recv(1024)
        #     recv_data += part
        #     if len(part) < 1024:
        #         break
        

        if not recv_data:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
        else:
            data.outb += recv_data

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            # ADD FUNCTIONALITY FOR OPERATIONS HERE 
            
            # if cmd == "signup":
            #     return_data = "GIVE US A USERNAME FUCKER"
            #     return_data = return_data.encode("utf-8")
            #     sent = sock.send(return_data)
            #     data.outb = data.outb[sent:]
            
            
            decoded_data = data.outb.decode("utf-8").strip()
            print("raw data:", data.outb, "decoded_data:", decoded_data)
            decoded_data = json.loads(decoded_data)
            # return_msg = decoded_data["message"] + " TESTTTT"

            # return_data = {"message": return_msg}

            # sent = write_socket(sock, return_data)
            # print(f"Sending {return_data} to {data.addr}")
            # data.outb = b''     # TODO: This is a hack to get it to work for now. This may be problematic if not all of the message is sent at once.

            if decoded_data["command"] == "send_chat":
                return_msg = decoded_data["message"] + " TESTTTT"

                return_data = {"message": return_msg}

                sent = write_socket(sock, return_data)
                print(f"Sending {return_data} to {data.addr}")
                data.outb = b''     # TODO: This is a hack to get it to work for now. This may be problematic if not all of the message is sent at once.


            elif decoded_data["command"] == "signup":
                return_data = {"message": "signup not implemented"}
                sent = write_socket(sock, return_data)
                print(f"Sending {return_data} to {data.addr}")
                data.outb = b''     # TODO: This is a hack to get it to work for now. This may be problematic if not all of the message is sent at once.



