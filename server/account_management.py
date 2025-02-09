import json 
import os 
import re
import time

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
        return {"success": False, "message": "Username and/or password cannot be empty."}
    if username_exists(username):
        return {"success": False, "message": "Username already exists. Please try again."}
    
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
    return {"success": True, "message": "Account created successfully."}

def login(username, password, host, port):
    existing_users = load_user_data()

    is_online = check_if_online(username)
    if is_online:
        return {"success": False, "message": "User is already logged in."}
        
    if username_exists(username):
        user = existing_users[username]
        if user["password"] == password:
            user["online"] = True
            user["host"] = host
            user["port"] = port
            save_user_data(existing_users)
            return {"success": True, "message": "Login successful."}
      
    return {"success": False, "message": "Incorrect username or password. Please try again."}

def logout(username):
    existing_users = load_user_data()

    if username_exists(username):
        user = existing_users[username]
        user["online"] = False
        user["host"] = ""
        user["port"] = ""
        save_user_data(existing_users)
        return {"success": True, "message": "Logout successful."}
      
    return {"success": False, "message": "Username does not exist."}

def list_accounts(username_pattern):
    existing_users = load_user_data()
    matching_users = [username for username in existing_users.keys() if re.search(username_pattern, username)]
    return {"success": True, "message": "Accounts listed successfully.", "matches": matching_users}

def send_offline_message(target_username, sender_username, message, timestamp):
    start = time.time()
    existing_users = load_user_data()
    db_pathname = get_db_pathname()

    # Find path to target user's unread messages
    target_db_pathname = os.path.join(db_pathname, "unread_messages", f"{target_username}.json")
    if not os.path.exists(target_db_pathname):
        return {"success": False, "message": "Target user does not exist."}

    new_message = {"message": message, "sender": sender_username, "timestamp": timestamp}
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

    end = time.time()
    print(f"Time to send offline message: {end - start} seconds")
    return {"success": True, "message": "Message sent successfully."}

def read_messages(username, num_messages):
    db_pathname = get_db_pathname()

    # Find path to target user's unread messages
    target_db_pathname = os.path.join(db_pathname, "unread_messages", f"{username}.json")
    if not os.path.exists(target_db_pathname):
        return {"success": False, "message": "Target user does not exist."}

    with open(target_db_pathname, "r") as f:
        unread_messages = json.load(f)
    
    with open(target_db_pathname, "w") as f:
        json.dump(unread_messages[num_messages:], f)
    
    return_data = {
        "success": True,
        "message": "Messages read successfully.",
        "messages": unread_messages[:num_messages]
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
    