import json

DATA_LENGTH_SIZE = 4
MAX_DATA_SIZE = 2**(DATA_LENGTH_SIZE * 8) - 1   # Maximum int that can be represented by 4 bytes

def read_socket(sock):
    '''
        Separates header from data and returns data as a bytestring. 
        Assumes data received from socket is JSON encoded.

        @param sock: socket object
    '''

    try:
        # Get length of data from first 4 bytes
        data_len = sock.recv(DATA_LENGTH_SIZE) 
        data_len = int.from_bytes(data_len, byteorder="big")

        # print(f"Data length: {data_len}")

        recv_data = sock.recv(data_len)
        return recv_data
        # if not recv_data:
        #     return None
        
        # recv_data = json.loads(recv_data.decode('utf-8'))
        # return recv_data

    # TODO: Implement more graceful error handling
    except Exception as e:
        print(f"Error reading from socket: {e}")
        raise e

def write_socket(sock, msg):
    '''
        Adds header to data and sends data through socket. Returns number of bytes sent
        @param sock: socket object
        @param msg: Python dictionary to send through socket
    '''

    try:
        msg_json = json.dumps(msg)

        # First 4 bytes sent indicates the length of the message
        msg_length = len(msg_json)
        msg_length_bytes = msg_length.to_bytes(DATA_LENGTH_SIZE, byteorder='big')
        full_message = msg_length_bytes + msg_json.encode('utf-8')

        sent = sock.send(full_message)

        # TODO: Make sure we never encounter this error?
        if (sent != len(full_message)):
            raise RuntimeError("Not all data sent")
        
        return sent
    
    # TODO: Implement more graceful error handling
    except Exception as e:
        print(f"Error writing to socket: {e}")
        raise e