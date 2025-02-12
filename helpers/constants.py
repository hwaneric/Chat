JSON_MODE = False

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
    "read_response": 13,
    "fetch_sent_messages": 14,
    "fetch_sent_messages_response": 15
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
    13: "read_response",
    14: "fetch_sent_messages",
    15: "fetch_sent_messages_response"
}