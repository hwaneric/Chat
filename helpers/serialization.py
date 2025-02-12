import json
from .constants import COMMANDS_TO_IDS, IDS_TO_COMMANDS, TOTAL_DATA_SIZE, DATA_LENGTH_SIZE, VERSION


def serialize(data, json_mode):
    if json_mode:
        data = json.dumps(data)
        data = data.encode('utf-8')

        # First byte indicates whether data is JSON encoded or not
        json_mode_bytes = json_mode.to_bytes(1, byteorder='big')

        # First 4 bytes sent indicates the length of the message
        data_length = len(data)
        data_length_bytes = data_length.to_bytes(DATA_LENGTH_SIZE, byteorder='big')
        full_message = json_mode_bytes + data_length_bytes + data
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

            message = data["message"].encode("utf-8")
            message_len = len(message).to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            data_serialization = sender_username_len + sender_username + target_username_len + target_username + timestamp + message_len + message
        
        case "register":
            username = data["username"].encode("utf-8")
            username_len = len(username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            host = data["host"].encode("utf-8")
            host_len = len(host).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            port = data["port"].to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = username_len + username + host_len + host + port
        
        case "read":
            username = data["username"].encode("utf-8")
            username_len = len(username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            try:
                num_messages = int(data["num_messages"])
            except ValueError:
                print("Number of requested messages was not an integer. Defaulting to 0.")
                num_messages = 0
            num_messages = num_messages.to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = username_len + username + num_messages
        
        case "delete_message":
            username = data["username"].encode("utf-8")
            username_len = len(username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            message_id = data["message_id"].encode("utf-8")
            message_id_len = len(message_id).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = username_len + username + message_id_len + message_id

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

            data_serialization = success + message_len + message + matches_bytes

        case "read_response":
            success = data["success"]
            success = success.to_bytes(1, byteorder="big")

            message = data["message"].encode("utf-8")
            message_len = len(message).to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            data_serialization = success + message_len + message
            data_serialization += serialize_message_list(data["messages"])
        
        case "fetch_sent_messages":
            username = data["username"].encode("utf-8")
            username_len = len(username).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
            data_serialization = username_len + username
        
        case "fetch_sent_messages_response":
            success = data["success"]
            success = success.to_bytes(1, byteorder="big")

            message = data["message"].encode("utf-8")
            message_len = len(message).to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            data_serialization = success + message_len + message

            sent_messages = data["sent_messages"]
            for recipient, messages in sent_messages.items():
                recipient_bytes = recipient.encode("utf-8")
                recipient_len = len(recipient_bytes).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
                data_serialization += recipient_len + recipient_bytes

                serialized_messages = serialize_message_list(messages)
                serialized_messages_len = len(serialized_messages).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
                data_serialization += serialized_messages_len + serialized_messages
        
        case "login_response":
            success = data["success"]
            success = success.to_bytes(1, byteorder="big")
            message = data["message"].encode("utf-8")
            message_len = len(message).to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            unread_message_count = data["unread_message_count"]
            unread_message_count = unread_message_count.to_bytes(DATA_LENGTH_SIZE, byteorder="big")

            data_serialization = success + message_len + message + unread_message_count

        case _:
            raise ValueError(f"Invalid command: {data['command']}")
        
    command_id = COMMANDS_TO_IDS[data["command"]]

    data_serialization = (
        json_mode.to_bytes(1, byteorder="big") + 
        command_id.to_bytes(1, byteorder="big") + 
        data_serialization
    )

    data_serialization_len = len(data_serialization).to_bytes(TOTAL_DATA_SIZE, byteorder="big")
    data_serialization = data_serialization_len + data_serialization
    serialization = VERSION.to_bytes(1, byteorder="big")
    serialization += data_serialization
    return serialization

def serialize_message_list(message_list):
    num_messages = len(message_list)
    num_messages = num_messages.to_bytes(DATA_LENGTH_SIZE, byteorder="big")

    data_serialization = num_messages

    for message in message_list:
        sender_bytes = message["sender"].encode("utf-8")
        sender_len = len(sender_bytes).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
       
        message_bytes = message["message"].encode("utf-8")
        message_len = len(message_bytes).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
        
        timestamp = message["timestamp"].to_bytes(DATA_LENGTH_SIZE, byteorder="big")
        
        message_id = message["message_id"].encode("utf-8")
        message_id_len = len(message_id).to_bytes(DATA_LENGTH_SIZE, byteorder="big")
        
        data_serialization += (
            sender_len + 
            sender_bytes + 
            message_len + 
            message_bytes + 
            timestamp + 
            message_id_len + 
            message_id
        )

    return data_serialization

def deserialize(data):
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

            password_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            password = data[index:].decode("utf-8")
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

            timestamp = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE

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

            port = int.from_bytes(data[index:], byteorder="big")
            return {"command": command, "username": username, "host": host, "port": port}

        case "read":
            username_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            username = data[index:index+username_len].decode("utf-8")
            index = index + username_len

            num_messages = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            return {"command": command, "username": username, "num_messages": num_messages}
        
        case "delete_message":
            username_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            username = data[index:index+username_len].decode("utf-8")
            index = index + username_len
            message_id_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            message_id = data[index:].decode("utf-8")
            return {"command": command, "username": username, "message_id": message_id}
        
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
            sender = data[index:index+sender_len].decode("utf-8")
            return {"success": success, "message": message, "sender": sender}
        
        case "list_response":
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
            while i < len(matches_str):
                char = matches_str[i]
                if char == ":":
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
            message = data[index:index+message_len].decode("utf-8")
            index = index + message_len
            messages = deserialize_message_list(data[index:])

            return {"success": success, "message": message, "messages": messages}

        case "fetch_sent_messages":
            username_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            username = data[index:index+username_len].decode("utf-8")
            return {"command": command, "username": username}

        case "fetch_sent_messages_response":
            success = bool.from_bytes(data[index:index+1], byteorder="big")
            index = index + 1

            message_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index += DATA_LENGTH_SIZE
            message = data[index:index+message_len].decode("utf-8")
            index += message_len

            # Format sent messages, keys are recipients, values are list of messages
            sent_messages = {}
            while index < len(data):
                recipient_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
                index += DATA_LENGTH_SIZE
                recipient = data[index:index+recipient_len].decode("utf-8")
                index += recipient_len

                serialized_messages_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
                index += DATA_LENGTH_SIZE
                messages = deserialize_message_list(data[index:index+serialized_messages_len])
                index += serialized_messages_len
                
                sent_messages[recipient] = messages
            
            return {"success": success, "message": message, "sent_messages": sent_messages}

        case "login_response":
            success = bool.from_bytes(data[index:index+1], byteorder="big")
            index = index + 1

            message_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            index = index + DATA_LENGTH_SIZE
            message = data[index:index+message_len].decode("utf-8")
            index += message_len

            unread_message_count = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
            return {"success": success, "message": message, "unread_message_count": unread_message_count}

        case _:
            raise ValueError(f"Invalid command: {command}")
    

def deserialize_message_list(data):
    num_messages = int.from_bytes(data[:DATA_LENGTH_SIZE], byteorder="big")
    index = DATA_LENGTH_SIZE

    messages = []
    for _ in range(num_messages):
        sender_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
        index += DATA_LENGTH_SIZE
        sender = data[index:index+sender_len].decode("utf-8")
        index += sender_len

        message_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
        index = index + DATA_LENGTH_SIZE
        message = data[index:index+message_len].decode("utf-8")
        index = index + message_len

        timestamp = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
        index += DATA_LENGTH_SIZE

        message_id_len = int.from_bytes(data[index:index+DATA_LENGTH_SIZE], byteorder="big")
        index += DATA_LENGTH_SIZE
        message_id = data[index:index+message_id_len].decode("utf-8")
        index += message_id_len

        messages.append({
            "sender": sender, 
            "message": message, 
            "timestamp": timestamp, 
            "message_id": message_id
        })

    return messages