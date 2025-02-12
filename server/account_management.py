import json 
import os 
import re
import time
import uuid

USER_DATA_FILE = "user_data.json"

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_data(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)


def username_exists(username):
    existing_users = load_user_data()

    return username in existing_users

def create_account(username, password, host, port): 
    existing_users = load_user_data()

    if not username or not password:
        return {
            "success": False, 
            "message": "Username and/or password cannot be empty.",
            "command": "server_response"
        }
    if username_exists(username):
        return {
            "success": False, 
            "message": "Username already exists. Please try again.",
            "command": "server_response"
        }
    
    existing_users[username] = {
        "username": username, 
        "password": password, 
        "online": True, 
        "host": host, 
        "port": port
    }

    save_user_data(existing_users)

    db_pathname = get_db_pathname()
    user_file_path = os.path.join(db_pathname, "unread_messages", f"{username}.json")
    with open(user_file_path, 'w') as user_file:
        json.dump([], user_file)
    return {
        "success": True, "message": 
        "Account created successfully.",
        "command": "server_response"
    }

def login(username, password, host, port):
    existing_users = load_user_data()

    is_online = check_if_online(username)
    if is_online:
        return {
            "success": False, 
            "message": "User is already logged in.",
            "command": "server_response"
        }
        
    if username_exists(username):
        user = existing_users[username]
        if user["password"] == password:
            user["online"] = True
            user["host"] = host
            user["port"] = port
            save_user_data(existing_users)

            # Get number of unread messages
            db_pathname = get_db_pathname()
            unread_messages_path = os.path.join(db_pathname, "unread_messages", f"{username}.json")
            unread_message_count = 0
            if os.path.exists(unread_messages_path):
                with open(unread_messages_path, "r") as f:
                    unread_messages = json.load(f)
                    unread_message_count = len(unread_messages)
            
            return {
                "success": True, 
                "message": "Login successful.",
                "command": "login_response",
                "unread_message_count": unread_message_count
            }
      
    return {
        "success": False, 
        "message": "Incorrect username or password. Please try again.",
        "command": "server_response"
    }

def logout(username):
    existing_users = load_user_data()

    if username_exists(username):
        user = existing_users[username]
        user["online"] = False
        user["host"] = ""
        user["port"] = ""
        save_user_data(existing_users)
        return {
            "success": True, 
            "message": "Logout successful.",
            "command": "server_response"
        }
      
    return {
        "success": False, 
        "message": "Username does not exist.",
        "command": "server_response"
    }

def list_accounts(username_pattern):
    try:
        existing_users = load_user_data()
        matching_users = [username for username in existing_users.keys() if re.search(username_pattern, username)]
        return {
            "success": True, 
            "message": "Accounts listed successfully.", 
            "matches": matching_users,
            "command": "list_response"
            }
    except re.PatternError:
        return {
            "success": False, 
            "message": "Invalid regex pattern.",
            "command": "server_response"
        }

def send_offline_message(target_username, sender_username, message, timestamp):
    start = time.time()
    existing_users = load_user_data()
    db_pathname = get_db_pathname()

    # Generate a unique message ID
    message_id = str(uuid.uuid4())

    # Find path to target user's unread messages
    target_db_pathname = os.path.join(db_pathname, "unread_messages", f"{target_username}.json")
    if not os.path.exists(target_db_pathname):
        return {
            "success": False, 
            "message": "Target user does not exist.", 
            "command": "server_response"
        }

    new_message = {"message_id": message_id, "message": message, "sender": sender_username, "timestamp": timestamp}
    with open(target_db_pathname, "r") as f:
        unread_messages = json.load(f)
    
    # Find the position to insert the new message to maintain sorted time order
    insert_position = len(unread_messages)
    for i in range(len(unread_messages) - 1, -1, -1):
        if unread_messages[i]["timestamp"] <= timestamp:
            insert_position = i + 1
            break

    # Insert the new message at the correct position
    unread_messages.insert(insert_position, new_message)
    with open(target_db_pathname, "w") as f:
        json.dump(unread_messages, f)

    # Save the sent message to the sender's sent messages
    sent_db_pathname = os.path.join(db_pathname, "sent_messages", f"{sender_username}.json")
    if not os.path.exists(sent_db_pathname):
        sent_messages = {}
    else:
        with open(sent_db_pathname, "r") as f:
            sent_messages = json.load(f)
    
    if target_username not in sent_messages:
        sent_messages[target_username] = []
    
    sent_messages[target_username].append(new_message)
    with open(sent_db_pathname, "w") as f:
        json.dump(sent_messages, f)

    end = time.time()
    print(f"Time to send offline message: {end - start} seconds")
    return {
        "success": True, 
        "message": "Message sent successfully.",
        "command": "server_response"
    }

def read_messages(username, num_messages):
    db_pathname = get_db_pathname()

    # Find path to target user's unread messages
    target_db_pathname = os.path.join(db_pathname, "unread_messages", f"{username}.json")
    if not os.path.exists(target_db_pathname):
        return {
            "success": False, 
            "message": "Target user does not exist.",
            "command": "server_response"
        }

    with open(target_db_pathname, "r") as f:
        unread_messages = json.load(f)
    
    with open(target_db_pathname, "w") as f:
        json.dump(unread_messages[num_messages:], f)
    
    return_data = {
        "success": True,
        "message": "Messages read successfully.",
        "messages": unread_messages[:num_messages],
        "command": "read_response"
    }
    return return_data

def check_if_online(username):
    existing_users = load_user_data()
    if username in existing_users:
        user = existing_users[username]
        return user["online"]
    
    return False
    # raise ValueError("Username does not exist.")

def get_db_pathname():
    current_dir = os.path.dirname(__file__)
    base_dir = os.path.dirname(current_dir)
    db_pathname = os.path.join(base_dir, 'db')
    return db_pathname

def logout_all_users():
    existing_users = load_user_data()
    for username in existing_users:
        user = existing_users[username]
        user["online"] = False
        user["host"] = ""
        user["port"] = ""
    save_user_data(existing_users)

def delete_account(username):
    existing_users = load_user_data()

    if username not in existing_users:
        return {
            "success": False, 
            "message": "Username does not exist.",
            "command": "server_response"
        }
    
    if existing_users[username]["online"]:
        del existing_users[username]
        save_user_data(existing_users)

        db_pathname = get_db_pathname()
        unread_messages_path = os.path.join(db_pathname, "unread_messages", f"{username}.json")
        if os.path.exists(unread_messages_path):
            os.remove(unread_messages_path)

        sent_messages_path = os.path.join(db_pathname, "sent_messages", f"{username}.json")
        if os.path.exists(sent_messages_path):
            os.remove(sent_messages_path)

        return {
            "success": True, 
            "message": "Account deleted successfully.",
            "command": "server_response"
        }
    
    return {
        "success": False, 
        "message": "Attempting to delete offline account.",
        "command": "server_response"
    }
    
def delete_message(username, message_id):
    db_pathname = get_db_pathname()

    # Load the user's sent messages
    sent_db_pathname = os.path.join(db_pathname, "sent_messages", f"{username}.json")
    if not os.path.exists(sent_db_pathname):
        return {"success": False, "message": "No sent messages found.", "command": "server_response"}
    
    with open(sent_db_pathname, "r") as f:
        sent_messages = json.load(f)
    
    # Find and delete the message with the given message_id
    target_username = None
    for recipient, messages in sent_messages.items():
        for message in messages: 
            if message["message_id"] == message_id:
                target_username = recipient
                break
        if target_username:
            break

    if not target_username: 
        return {"success": False, "message": "Message ID not found.", "command": "server_response"}
    
    # Remove message from sent_messages
    sent_messages[target_username] = [msg for msg in sent_messages[target_username] if msg["message_id"] != message_id]
    with open(sent_db_pathname, "w") as f:
        json.dump(sent_messages, f)

    # Load the target user's unread messages
    target_db_pathname = os.path.join(db_pathname, "unread_messages", f"{target_username}.json")
    if not os.path.exists(target_db_pathname):
        return {"success": False, "message": "Target user does not exist.", "command": "server_response"}
    
    with open(target_db_pathname, "r") as f:
        unread_messages = json.load(f)

    # Remove message from target user's unread_messages
    unread_messages = [msg for msg in unread_messages if msg["message_id"] != message_id]
    with open(target_db_pathname, "w") as f:
        json.dump(unread_messages, f)

    return {"success": True, "message": "Message deleted successfully.", "command": "server_response"}


def fetch_sent_messages(username):
    db_pathname = get_db_pathname()
    sent_db_pathname = os.path.join(db_pathname, "sent_messages", f"{username}.json")
    if not os.path.exists(sent_db_pathname):
        return {"success": False, "message": "No sent messages found.", "command": "server_response"}

    with open(sent_db_pathname, "r") as f:
        sent_messages = json.load(f)
    return {"success": True, "sent_messages": sent_messages, "message": "Sent messages fetched successfully.", "command": "fetch_sent_messages_response"}

