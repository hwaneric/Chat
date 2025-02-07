import json
import sys
sys.path.append('../')
from helpers.socket_io import read_socket, write_socket

def attempt_signup(client_sock, username, password):
    msg_data = {"username": username, "password": password, "command": "signup"}

    sent = write_socket(client_sock, msg_data)
    data = read_socket(client_sock)

    if not data:
        return {"success": False, "message": "Server side error while attempting signup. Please try again!"}

    data = data.decode("utf-8")
    data = json.loads(data)
    return {"success": False, "message": data["message"]}   # TODO: Make this actually correspond to what server responded
  
def attempt_login(client_sock, username, password):
    msg_data = {"command": "login", "username": username, "password": password}

    sent = write_socket(client_sock, msg_data)
    data = read_socket(client_sock)

    if not data:
        return {"success": False, "message": "Server side error while attempting login. Please try again!"}

    data = data.decode("utf-8")
    data = json.loads(data)
    return {"success": False, "message": data["message"]}   # TODO: Make this actually correspond to what server responded
  