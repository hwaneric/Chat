DATA_LENGTH_SIZE = 4
MAX_DATA_SIZE = 2**(DATA_LENGTH_SIZE * 8) - 1   # Maximum int that can be represented by 4 bytes

# Separates header from data and returns data from socket as a bytestring
def read_socket(sock):
    data_len = sock.recv(DATA_LENGTH_SIZE) # First 4 bytes reserved for data length
    data_len = int.from_bytes(data_len, byteorder="big")
    print(f"Data length: {data_len}")

    recv_data = sock.recv(data_len)
    return recv_data

# Adds header to data and send data through socket. Return number of bytes sent
def write_socket(sock, message):
    message_length = len(message)
    message_length_bytes = message_length.to_bytes(DATA_LENGTH_SIZE, byteorder='big')

    full_message = message_length_bytes + message.encode('utf-8')
    sent = sock.send(full_message)
    
    return sent