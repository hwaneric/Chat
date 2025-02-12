import pytest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('../')
from client.client import Client

def test_connect_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    with patch("socket.socket.connect") as mock_connect:
        mock_connect.return_value = None
        client.connect()
        mock_connect.assert_called_once_with(("127.0.0.1", 12345))

def test_connect_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    with patch("socket.socket.connect", side_effect=Exception("Connection error")) as mock_connect:
        with pytest.raises(SystemExit):
            client.connect()
        mock_connect.assert_called_once_with(("127.0.0.1", 12345))

def test_signup_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": true}'
        mock_deserialize.return_value = {"success": True}
        
        success, message = client.signup("testuser", "password123")
        
        assert success == True
        assert message == "Successfully signed up!"
        assert client.username == "testuser"

def test_signup_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": false, "message": "Username already exists."}'
        mock_deserialize.return_value = {"success": False, "message": "Username already exists."}
        
        success, message = client.signup("testuser", "password123")
        
        assert success == False
        assert message == "Username already exists."
        assert client.username == None

def test_signup_server_error():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = None
        
        success, message = client.signup("testuser", "password123")
        
        assert success == False
        assert message == "Server side error while attempting signup. Please try again!"
        assert client.username == None
        

def test_login_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": true, "unread_message_count": 5}'
        mock_deserialize.return_value = {"success": True, "unread_message_count": 5}
        
        success, message, unread_message_count = client.login("testuser", "password123")
        
        assert success == True
        assert message == "Successfully logged in!"
        assert unread_message_count == 5
        assert client.username == "testuser"

def test_login_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": false, "message": "Incorrect username or password. Please try again."}'
        mock_deserialize.return_value = {"success": False, "message": "Incorrect username or password. Please try again."}
        
        success, message, unread_message_count = client.login("testuser", "wrongpassword")
        
        assert success == False
        assert message == "Incorrect username or password. Please try again."
        assert unread_message_count == -1
        assert client.username == None

def test_login_server_error():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = None
        
        success, message, unread_message_count = client.login("testuser", "password123")
        
        assert success == False
        assert message == "Server side error while attempting login. Please try again!"
        assert unread_message_count == -1
        assert client.username == None

def test_list_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": true, "matches": ["user1", "user2"]}'
        mock_deserialize.return_value = {"success": True, "matches": ["user1", "user2"]}
        
        success, matches = client.list("user")
        
        assert success == True
        assert matches == ["user1", "user2"]

def test_list_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": false, "message": "No users found."}'
        mock_deserialize.return_value = {"success": False, "message": "No users found."}
        
        success, message = client.list("nonexistentuser")
        
        assert success == False
        assert message == "No users found."

def test_list_server_error():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = None
        
        success, message = client.list("user")
        
        assert success == False
        assert message == "Server side error while attempting to list users. Please try again!"

def test_message_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": true}'
        mock_deserialize.return_value = {"success": True}
        
        success, message = client.message("targetuser", "Hello, World!")
        
        assert success == True
        assert message == "Message sent successfully to targetuser!"

def test_message_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": false, "message": "User not found."}'
        mock_deserialize.return_value = {"success": False, "message": "User not found."}
        
        success, message = client.message("nonexistentuser", "Hello, World!")
        
        assert success == False
        assert message == "User not found."

def test_message_server_error():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = None
        
        success, message = client.message("targetuser", "Hello, World!")
        
        assert success == False
        assert message == "Server side error while attempting to send message. Please try again!"

def test_logout_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": true}'
        mock_deserialize.return_value = {"success": True}
        
        success, message = client.logout()
        
        assert success == True
        assert message == "Successfully logged out!"
        assert client.username == None

def test_logout_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": false, "message": "Logout failed."}'
        mock_deserialize.return_value = {"success": False, "message": "Logout failed."}
        
        success, message = client.logout()
        
        assert success == False
        assert message == "Logout failed."
        assert client.username == "testuser"

def test_logout_server_error():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = None
        
        success, message = client.logout()
        
        assert success == False
        assert message == "Server side error while attempting to logout. Please try again!"
        assert client.username == "testuser"

def test_read_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": true, "messages": [{"sender": "user1", "timestamp": 1617184800, "message": "Hello!"}]}'
        mock_deserialize.return_value = {"success": True, "messages": [{"sender": "user1", "timestamp": 1617184800, "message": "Hello!"}]}
        
        success, messages = client.read(1)
        
        # Print the deserialized data
        print("Deserialized data:", mock_deserialize.return_value)
        print("Messages:", messages)
        
        assert success == True
        assert messages == ["user1 at (03-31-2021, 12:00 AM): Hello!"]

def test_read_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": false, "message": "No messages found."}'
        mock_deserialize.return_value = {"success": False, "message": "No messages found."}
        
        success, message = client.read(1)
        
        assert success == False
        assert message == "No messages found."

def test_read_server_error():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = None
        
        success, message = client.read(1)
        
        assert success == False
        assert message == "Server side error while attempting to read messages. Please try again!"

def test_delete_account_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": true}'
        mock_deserialize.return_value = {"success": True}
        
        success, message = client.delete_account()
        
        # Print the deserialized data
        print("Deserialized data:", mock_deserialize.return_value)
        
        assert success == True
        assert message == "Successfully deleted account!"
        assert client.username == None

def test_delete_account_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": false, "message": "Delete account failed."}'
        mock_deserialize.return_value = {"success": False, "message": "Delete account failed."}
        
        success, message = client.delete_account()
        
        assert success == False
        assert message == "Delete account failed."
        assert client.username == "testuser"

def test_delete_account_server_error():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = None
        
        success, message = client.delete_account()
        
        assert success == False
        assert message == "Server side error while attempting to delete account. Please try again!"
        assert client.username == "testuser"

def test_fetch_sent_messages_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": true, "sent_messages": ["Message 1", "Message 2"]}'
        mock_deserialize.return_value = {"success": True, "sent_messages": ["Message 1", "Message 2"]}
        
        success, sent_messages = client.fetch_sent_messages()
        
        # Print the deserialized data
        print("Deserialized data:", mock_deserialize.return_value)
        
        assert success == True
        assert sent_messages == ["Message 1", "Message 2"]

def test_fetch_sent_messages_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": false, "message": "Fetch sent messages failed."}'
        mock_deserialize.return_value = {"success": False, "message": "Fetch sent messages failed."}
        
        success, message = client.fetch_sent_messages()
        
        assert success == False
        assert message == "Fetch sent messages failed."

def test_fetch_sent_messages_server_error():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = None
        
        success, message = client.fetch_sent_messages()
        
        assert success == False

def test_delete_message_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": true}'
        mock_deserialize.return_value = {"success": True}
        
        success, message = client.delete_message(1)
        
        # Print the deserialized data
        print("Deserialized data:", mock_deserialize.return_value)
        
        assert success == True
        assert message == "Successfully deleted message 1!"

def test_delete_message_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": false, "message": "Delete message failed."}'
        mock_deserialize.return_value = {"success": False, "message": "Delete message failed."}
        
        success, message = client.delete_message(1)
        
        assert success == False
        assert message == "Delete message failed."

def test_delete_message_server_error():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = None
        
        success, message = client.delete_message(1)
        
        assert success == False
        assert message == "Server side error while attempting to delete message. Please try again!"