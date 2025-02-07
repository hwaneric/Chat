import json 
import os 
import re

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

def create_account(username, password): 
    existing_users = load_user_data()

    if not username or not password:
        return {"success": False, "message": "Username and/or password cannot be empty."}
    if username_exists(username):
        return {"success": False, "message": "Username already exists. Please try again."}
    else:
        existing_users[username] = {"username": username, "password": password}
        save_user_data(existing_users)
        return {"success": True, "message": "Account created successfully."}

def login(username, password):
    existing_users = load_user_data()

    if username_exists(username):
        user = existing_users[username]
        if user["password"] == password:
            return {"success": True, "message": "Login successful."}
      
    return {"success": False, "message": "Incorrect username or password. Please try again."}

def list_accounts(username_pattern):
    existing_users = load_user_data()
    matching_users = [username for username in existing_users.keys() if re.search(username_pattern, username)]
    return {"success": True, "message": "Accounts listed successfully.", "matches": matching_users}