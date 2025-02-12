import pytest
from unittest.mock import patch
import sys
sys.path.append('../')
from client.client import Client

def test_connect_success():
    client = Client("127.0.0.1", 12345)
    with patch("socket.socket.connect") as mock_connect:
        mock_connect.return_value = None
        client.connect()
        mock_connect.assert_called_once_with(("127.0.0.1", 12345))

def test_connect_failure():
    client = Client("127.0.0.1", 12345)
    with patch("socket.socket.connect", side_effect=Exception("Connection error")) as mock_connect:
        with pytest.raises(SystemExit):
            client.connect()
        mock_connect.assert_called_once_with(("127.0.0.1", 12345))

def test_signup_success():
    client = Client("127.0.0.1", 12345)
    
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
    client = Client("127.0.0.1", 12345)
    
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
    client = Client("127.0.0.1", 12345)
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = None
        
        success, message = client.signup("testuser", "password123")
        
        assert success == False
        assert message == "Server side error while attempting signup. Please try again!"
        assert client.username == None
        
def test_login_success():
    client = Client("127.0.0.1", 12345)
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": true}'
        mock_deserialize.return_value = {"success": True}
        
        success, message = client.login("testuser", "password123")

        print("Deserialization data:", mock_deserialize.return_value)
        
        assert success == True
        assert message == "Successfully logged in!"
        assert client.username == "testuser"





# COPY AND PASTED:
def test_login_success():
    client = Client("127.0.0.1", 12345)
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket, \
         patch("client.client.deserialize") as mock_deserialize:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = b'{"success": true, "unread_message_count": 5}'
        mock_deserialize.return_value = {"success": True, "unread_message_count": 5}
        
        success, message, unread_message_count = client.login("testuser", "password123")
        
        # Print the deserialized data
        print("Deserialized data:", mock_deserialize.return_value)
        
        assert success == True
        assert message == "Successfully logged in!"
        assert unread_message_count == 5
        assert client.username == "testuser"

def test_login_failure():
    client = Client("127.0.0.1", 12345)
    
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
    client = Client("127.0.0.1", 12345)
    
    with patch("client.client.write_socket") as mock_write_socket, \
         patch("client.client.read_socket") as mock_read_socket:
        
        mock_write_socket.return_value = None
        mock_read_socket.return_value = None
        
        success, message, unread_message_count = client.login("testuser", "password123")
        
        assert success == False
        assert message == "Server side error while attempting login. Please try again!"
        assert unread_message_count == -1
        assert client.username == None