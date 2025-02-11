import json


TOTAL_DATA_SIZE = 8
DATA_LENGTH_SIZE = 4
MAX_DATA_SIZE = 2**(DATA_LENGTH_SIZE * 8) - 1   # Maximum int that can be represented by 4 bytes
VERSION = 1

COMMANDS_TO_IDS = {
    "signup": 0,
    "login": 1,
    "logout": 2,
    "list": 3,
    "message": 4,
    "register": 5,
    "read": 6,
    "delete_account": 7,
    "delete_message": 8,
    "server_response": 9,
    "online_message": 10,
    "list": 11,
    "list_response": 12,
    "read_response": 13
}

IDS_TO_COMMANDS = {
    0: "signup",
    1: "login",
    2: "logout",
    3: "list",
    4: "message",
    5: "register",
    6: "read",
    7: "delete_account",
    8: "delete_message",
    9: "server_response",
    10: "online_message",
    11: "list",
    12: "list_response",
    13: "read_response"
}

def read_socket(sock, json_mode=False):
    '''
        Separates header from data and returns data as a bytestring. 
        Assumes data received from socket is JSON encoded.

        @param sock: socket object
    '''

    try:
        if json_mode:
            # Get length of data from first 4 bytes
            data_len = sock.recv(DATA_LENGTH_SIZE) 
            data_len = int.from_bytes(data_len, byteorder="big")

            recv_data = sock.recv(data_len)

            return recv_data
            # if return_bytestring:
            #     return recv_data
            
            # recv_data = recv_data.decode("utf-8")

            # if not recv_data:
            #     return None
            
            # return json.loads(recv_data)
        
        else:
            version_number = sock.recv(1)

            # No data received. Indicates client has disconnected. Exit function
            if version_number == b'':
                return None
            
            version_number = int.from_bytes(version_number, byteorder="big")
            if version_number != VERSION:
                data = sock.recv(1024)
                raise ValueError(f"Invalid version number: {version_number}")

            data_size = sock.recv(TOTAL_DATA_SIZE)
            data_size = int.from_bytes(data_size, byteorder="big")

            data = sock.recv(data_size)
            return data



    # TODO: Implement more graceful error handling
    except Exception as e:
        print(f"Error reading from socket: {e}")
        raise e

def write_socket(sock, msg, json_mode=False):
    '''
        Adds header to data and sends data through socket. Returns number of bytes sent
        @param sock: socket object
        @param msg: Python dictionary to send through socket
    '''
    try:
        full_message = serialize(msg, json_mode)

        sent = sock.send(full_message)

        # TODO: Make sure we never encounter this error?
        if (sent != len(full_message)):
            raise RuntimeError("Not all data sent")
        
        return sent
        
    
    # TODO: Implement more graceful error handling
    except Exception as e:
        print(f"Error writing to socket: {e}")
        raise e
    

def serialize(data, json_mode):
    if json_mode:
        msg_json = json.dumps(data)
        # First byte indicates whether data is JSON encoded or not
        json_mode_bytes = json_mode.to_bytes(1, byteorder='big')

        # First 4 bytes sent indicates the length of the message
        msg_length = len(msg_json)
        msg_length_bytes = msg_length.to_bytes(DATA_LENGTH_SIZE, byteorder='big')
        full_message = json_mode_bytes + msg_length_bytes + msg_json.encode('utf-8')
        return full_message

    match data["command"]:
        case "signup" | "login":
            username = data["username"].encode("utf-8")
            username_len = len(username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            password = data["password"].encode("utf-8")
            password_len = len(password).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = username_len + username + password_len + password
            
        case "logout" | "delete_account":
            username = data["username"].encode("utf-8")
            username_len = len(username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = username_len + username

        case "list":
            username_pattern = data["username_pattern"].encode("utf-8")
            username_pattern_len = len(username_pattern).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = username_pattern_len + username_pattern
        
        case "message":
            TIMESTAMP_SIZE = 4 # 4 bytes
            sender_username = data["sender_username"].encode("utf-8")
            sender_username_len = len(sender_username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            target_username = data["target_username"].encode("utf-8")
            target_username_len = len(target_username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            timestamp = data["timestamp"].to_bytes(TIMESTAMP_SIZE, byteorder="big")
            timestamp_len = TIMESTAMP_SIZE.to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            message = data["message"].encode("utf-8")
            message_len = len(message).to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            data_serialization = sender_username_len + sender_username + target_username_len + target_username + timestamp_len + timestamp + message_len + message
        
        case "register":
            username = data["username"].encode("utf-8")
            username_len = len(username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            host = data["host"].encode("utf-8")
            host_len = len(host).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            port = data["port"].to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = username_len + username + host_len + host + port
        
        case "read":
            NUM_MESSAGES_SIZE = 4 # 4 bytes
            username = data["username"].encode("utf-8")
            username_len = len(username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            num_messages = int(data["num_messages"])
            num_messages = num_messages.to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            num_messages_len = NUM_MESSAGES_SIZE.to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = username_len + username + num_messages_len + num_messages
        
        case "delete_message":
            sender_username = data["sender_username"].encode("utf-8")
            sender_username_len = len(sender_username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            target_username = data["target_username"].encode("utf-8")
            target_username_len = len(target_username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            message_id = data["message_id"].encode("utf-8")
            message_id_len = len(message_id).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = sender_username_len + sender_username + target_username_len + target_username + message_id_len + message_id

        case "server_response":
            success = data["success"]
            success = success.to_bytes(1, byteorder="big")
            message = data["message"].encode("utf-8")
            message_len = len(message).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = success + message_len + message
        
        case "online_message":
            success = data["success"]
            success = success.to_bytes(1, byteorder="big")
            message = data["message"].encode("utf-8")
            message_len = len(message).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            sender = data["sender"].encode("utf-8")
            sender_len = len(sender).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = success + message_len + message + sender_len + sender
        
        case "list_response":
            success = data["success"]
            success = success.to_bytes(1, byteorder="big")
            message = data["message"].encode("utf-8")
            message_len = len(message).to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            matches_str = ""
            matches = data["matches"]
            for match in matches:
                matches_str += f"{len(match)}:{match}"
            matches_bytes = matches_str.encode("utf-8")
            # matches_len = len(matches_bytes).to_bytes(DATA_LENGTH_SIZE, byteorder="big") 

            data_serialization = success + message_len + message + matches_bytes

        case "read_response":
            #TODO: HANDLE READ RESPONSE HERE
            success = data["success"]
            success = success.to_bytes(1, byteorder="big")

            message = data["message"].encode("utf-8")
            message_len = len(message).to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            num_messages = len(data["messages"])
            num_messages = num_messages.to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            # num_messages_len = len(num_messages).to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            data_serialization = success + message_len + message + num_messages

            messages = data["messages"]
            for message in messages:
                sender_bytes = message["sender"].encode("utf-8")
                sender_len = len(sender_bytes).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
                message_bytes = message["message"].encode("utf-8")
                message_len = len(message_bytes).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
                timestamp = message["timestamp"].to_bytes(DATA_LENGTH_SIZE, byteorder="big")
                data_serialization += sender_len + sender_bytes + message_len + message_bytes + timestamp

        case _:
            raise ValueError(f"Invalid command: {data['command']}")
        
    command_id = COMMANDS_TO_IDS[data["command"]]
    data_serialization = json_mode.to_bytes(1, byteorder="big") + command_id.to_bytes(1, byteorder="big") + data_serialization
    # data_serialization += command_id.to_bytes(1, byteorder="big")
    print("command_id", command_id, "data_serialization", data_serialization)
    data_serialization_len = len(data_serialization).to_bytes(TOTAL_DATA_SIZE, byteorder="big")
    print("data_serialization", data_serialization, "data_serialization_len", data_serialization_len)
    serialization = b""
    serialization += VERSION.to_bytes(1, byteorder="big")
    serialization += data_serialization_len + data_serialization
    print("data that was serialized", data, "serialization:", serialization)
    return serialization

def deserialize(data):
    print("deserializing data", data)
    json_mode = bool.from_bytes(data[:1], byteorder="big")
    if json_mode:
        return json.loads(data[1:])
    
    command_id = int.from_bytes(data[1:2], byteorder="big")
    command = IDS_TO_COMMANDS[command_id]

    index = 2
    match command:
        case "signup" | "login":
            username_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            username = data[index:index+username_len].decode("utf-8")
            index = index + username_len
            print(username_len, username)

            password_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            password = data[index:].decode("utf-8")
            print(password_len, password)
            return {"command": command, "username": username, "password": password}
        
        case "logout" | "delete_account":
            username_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            username = data[index:].decode("utf-8")
            return {"command": command, "username": username}
        
        case "list":
            username_pattern_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE

            username_pattern = data[index:].decode("utf-8")
            return {"command": command, "username_pattern": username_pattern}

        case "message":
            sender_username_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            sender_username = data[index:index+sender_username_len].decode("utf-8")
            index = index + sender_username_len

            target_username_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            target_username = data[index:index+target_username_len].decode("utf-8")
            index = index + target_username_len

            timestamp_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            timestamp = int.from_bytes(data[index:index+timestamp_len], byteorder="big")
            index = index + timestamp_len

            message_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            message = data[index:].decode("utf-8")
            return {"command": command, "sender_username": sender_username, "target_username": target_username, "timestamp": timestamp, "message": message}

        case "register":
            username_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            username = data[index:index+username_len].decode("utf-8")
            index = index + username_len

            host_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            host = data[index:index+host_len].decode("utf-8")
            index = index + host_len

            # port_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            # index = index + DATA_LENGTH_SIZE
            port = int.from_bytes(data[index:], byteorder="big")
            return {"command": command, "username": username, "host": host, "port": port}

        case "read":
            username_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            username = data[index:index+username_len].decode("utf-8")
            index = index + username_len

            num_messages_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            num_messages = int.from_bytes(data[index:index+num_messages_len], byteorder="big")
            return {"command": command, "username": username, "num_messages": num_messages}
        
        case "delete_message":
            sender_username_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            sender_username = data[index:index+sender_username_len].decode("utf-8")
            index = index + sender_username_len

            target_username_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            target_username = data[index:index+target_username_len].decode("utf-8")
            index = index + target_username_len

            message_id_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            message_id = data[index:].decode("utf-8")
            return {"command": command, "sender_username": sender_username, "target_username": target_username, "message_id": message_id}
        
        case "server_response":
            success = bool.from_bytes(data[index:index+1], byteorder="big")
            index = index + 1

            message_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            message = data[index:].decode("utf-8")
            return {"success": success, "message": message}
        
        case "online_message":
            success = bool.from_bytes(data[index:index+1], byteorder="big")
            index = index + 1

            message_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            message = data[index:index+message_len].decode("utf-8")
            index = index + message_len

            sender_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            sender = data[index:].decode("utf-8")
            return {"success": success, "message": message, "sender": sender}
        
        case "list_response":
            print('in list response deserialzation')
            success = bool.from_bytes(data[index:index+1], byteorder="big")
            index = index + 1

            message_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            message = data[index:index+message_len].decode("utf-8")
            index = index + message_len

            # Decode array of strings
            matches_str = data[index:]
            matches_str = matches_str.decode("utf-8")
            match_len = ""
            matches = []
            i = 0
            print("matches_str", matches_str, len(matches_str))
            while i < len(matches_str):
                char = matches_str[i]
                if char == ":":
                    print("match_len", match_len, i)
                    match_len = int(match_len)
                    matches.append(matches_str[i+1:i+1+match_len])
                    i += match_len + 1
                    match_len = ""

                else:
                    match_len += char
                    i += 1
        
            return {"success": success, "message": message, "matches": matches}

        case "read_response":
            success = bool.from_bytes(data[index:index+1], byteorder="big")
            index = index + 1

            message_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            message = data[index:index+DATA_LENGTH_SIZE].decode("utf-8")
            index = index + message_len

            num_messages = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE


            messages = []
            for i in range(num_messages):
                sender_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
                index = index + DATA_LENGTH_SIZE
                sender = data[index:index+sender_len].decode("utf-8")
                index = index + sender_len

                message_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
                index = index + DATA_LENGTH_SIZE
                message = data[index:index+message_len].decode("utf-8")
                index = index + message_len

                timestamp = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
                index += DATA_LENGTH_SIZE

                messages.append({"sender": sender, "message": message, "timestamp": timestamp})
            return {"success": success, "message": message, "messages": messages}

        case _:
            raise ValueError(f"Invalid command: {command}")
    

