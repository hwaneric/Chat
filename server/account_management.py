import json 
import os 

USER_DATA_FILE = "user_data.json"

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_data(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)

existing_users = load_user_data()

def username_exists(username):
    return username in existing_users

def create_account(username, password): 
    if username_exists(username):
        return {"success": False, "message": "Username already exists. Please try again."}
    else:
        existing_users[username] = {"username": username, "password": password}
        save_user_data(existing_users)
        return {"success": True, "message": "Account created successfully."}

def login(username, password):
    if username_exists(username) and existing_users[username] == password:
        return {"success": True, "message": "Login successful."}
    else:
        return {"success": False, "message": "Incorrect username or password. Please try again."}