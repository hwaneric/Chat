from .constants import DATA_LENGTH_SIZE, TOTAL_DATA_SIZE, VERSION, JSON_MODE
from .serialization import serialize

def read_socket(sock):
    '''
        Separates header from data and returns data as a bytestring. 
        Assumes data received from socket is JSON encoded.

        @param sock: socket object
    '''

    try:
        if JSON_MODE:
            # Get length of data from first 4 bytes
            data_len = sock.recv(DATA_LENGTH_SIZE) 
            data_len = int.from_bytes(data_len, byteorder="big")

            recv_data = sock.recv(data_len)

            return recv_data
        
        else:
            version_number = sock.recv(1)

            # No data received. Indicates client has disconnected. Exit function
            if version_number == b'':
                return None
            
            version_number = int.from_bytes(version_number, byteorder="big")
            if version_number != VERSION:
                data = sock.recv(1024)
                print("data before version error", data)
                raise ValueError(f"Invalid version number: {version_number}")

            data_size = sock.recv(TOTAL_DATA_SIZE)
            data_size = int.from_bytes(data_size, byteorder="big")

            data = sock.recv(data_size)
            return data

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
        full_message = serialize(msg, JSON_MODE)
        sent = sock.send(full_message)

        if (sent != len(full_message)):
            raise RuntimeError("Not all data sent")
        
        return sent
        
    
    except Exception as e:
        print(f"Error writing to socket: {e}")
        raise e
    