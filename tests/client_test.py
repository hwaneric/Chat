import pytest
from unittest.mock import patch, MagicMock, ANY
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../client')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../protos')))
from client import Client
import server_pb2
import server_pb2_grpc

def test_signup_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")

    with patch.object(client.stub, 'Signup') as mock_signup:
        mock_signup.return_value = server_pb2.StandardServerResponse(success=True, message="Successfully signed up!")
        success, message = client.signup("testuser", "password123")

        assert success == True
        assert message == "Successfully signed up!"
        assert client.username == "testuser"
        mock_signup.assert_called_once_with(server_pb2.UserAuthRequest(username="testuser", password="password123"))

def test_signup_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    
    with patch.object(client.stub, 'Signup') as mock_signup:
        mock_signup.return_value = server_pb2.StandardServerResponse(success=False, message="Username already exists.")
        success, message = client.signup("testuser", "password123")
        
        assert success == False
        assert message == "Username already exists."
        assert client.username == None
        mock_signup.assert_called_once_with(server_pb2.UserAuthRequest(username="testuser", password="password123"))

# def test_signup_server_error():
#     client = Client("127.0.0.1", 12345, "127.0.0.1")

#     with patch.object(client.stub, 'Signup') as mock_signup:
#         mock_signup.return_value = None
#         success, message = client.signup("testuser", "password123")

#         assert success == False
#         assert message == "Server side error while attempting signup. Please try again!"
#         assert client.username == None
#         mock_signup.assert_called_once_with(server_pb2.UserAuthRequest(username="testuser", password="password123"))     

def test_login_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")

    response = server_pb2.UserLoginResponse()
    response.success.CopyFrom(server_pb2.UserLoginSuccess(success=True, message="Successfully logged in!", unread_message_count=5))

    with patch.object(client.stub, 'Login', return_value=response) as mock_login:
        success, message, unread_message_count = client.login("testuser", "password123")

        assert success == True
        assert message == "Successfully logged in!"
        assert unread_message_count == 5
        assert client.username == "testuser"
        mock_login.assert_called_once_with(server_pb2.UserAuthRequest(username="testuser", password="password123"))

def test_login_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")

    response = server_pb2.UserLoginResponse()
    response.failure.CopyFrom(server_pb2.StandardServerResponse(success=False, message="Invalid credentials."))

    with patch.object(client.stub, 'Login', return_value=response) as mock_login:
        success, message, unread_message_count = client.login("testuser", "wrongpassword")

        assert success == False
        assert message == "Invalid credentials."
        assert unread_message_count == -1
        assert client.username == None
        mock_login.assert_called_once_with(server_pb2.UserAuthRequest(username="testuser", password="wrongpassword"))

# def test_login_server_error():
#     client = Client("127.0.0.1", 12345, "127.0.0.1")

#     response = server_pb2.UserLoginResponse()
#     response.failure.CopyFrom(server_pb2.StandardServerResponse(success=False, message="Server side error while attempting login. Please try again!"))

#     with patch.object(client.stub, 'Login') as mock_login:
#         mock_login.return_value = None
#         success, message, unread_message_count = client.login("testuser", "password123")

#         assert success == False
#         assert message == "Server side error while attempting login. Please try again!"
#         assert unread_message_count == -1
#         assert client.username == None
#         mock_login.assert_called_once_with(server_pb2.UserAuthRequest(username="testuser", password="password123"))

def test_list_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"

    response = server_pb2.ListUsernamesResponse()
    response.success.CopyFrom(server_pb2.ListUsernames(success=True, message="Accounts listed successfully.", matches=["user1", "user2"]))

    with patch.object(client.stub, 'ListUsernames', return_value=response) as mock_list:
        success, matches = client.list("user")
        assert success == True
        assert matches == ["user1", "user2"]
        assert client.username == "testuser"
        mock_list.assert_called_once_with(server_pb2.ListUsernamesRequest(username_pattern="user"))

def test_list_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"

    response = server_pb2.ListUsernamesResponse()
    response.failure.CopyFrom(server_pb2.StandardServerResponse(success=False, message="Invalid regex pattern."))
    with patch.object(client.stub, 'ListUsernames', return_value=response) as mock_list:
        success, message = client.list("?")

        assert success == False
        assert message == "Invalid regex pattern."
        assert client.username == "testuser"
        mock_list.assert_called_once_with(server_pb2.ListUsernamesRequest(username_pattern="?"))

# def test_list_server_error():
#     client = Client("127.0.0.1", 12345, "127.0.0.1")
#     client.username = "testuser"
    
#     with patch("client.client.write_socket") as mock_write_socket, \
#          patch("client.client.read_socket") as mock_read_socket:
        
#         mock_write_socket.return_value = None
#         mock_read_socket.return_value = None
        
#         success, message = client.list("user")
        
#         assert success == False
#         assert message == "Server side error while attempting to list users. Please try again!"

def test_message_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"

    with patch.object(client.stub, 'SendMessage', return_value=server_pb2.StandardServerResponse(success=True, message="Message sent successfully.")) as mock_message:
        success, message = client.message("targetuser", "Hello")

        assert success == True
        assert message == "Message sent successfully."
        assert client.username == "testuser"

        actual_call_args = mock_message.call_args[0][0]

        assert actual_call_args.sender_username == "testuser"
        assert actual_call_args.target_username == "targetuser"
        assert actual_call_args.message == "Hello"
        current_time = int(time.time())
        assert current_time - actual_call_args.timestamp <= 5

def test_message_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"

    with patch.object(client.stub, 'SendMessage', return_value=server_pb2.StandardServerResponse(success=False, message="Target user does not exist.")) as mock_message:
        success, message = client.message("nonexistentuser", "Hello")

        assert success == False
        assert message == "Target user does not exist."
        assert client.username == "testuser"

        actual_call_args = mock_message.call_args[0][0]

        assert actual_call_args.sender_username == "testuser"
        assert actual_call_args.target_username == "nonexistentuser"
        assert actual_call_args.message == "Hello"
        current_time = int(time.time())
        assert current_time - actual_call_args.timestamp <= 5

# def test_message_server_error():
#     client = Client("127.0.0.1", 12345, "127.0.0.1")
#     client.username = "testuser"
    
#     with patch("client.client.write_socket") as mock_write_socket, \
#          patch("client.client.read_socket") as mock_read_socket:
        
#         mock_write_socket.return_value = None
#         mock_read_socket.return_value = None
        
#         success, message = client.message("targetuser", "Hello, World!")
        
#         assert success == False
#         assert message == "Server side error while attempting to send message. Please try again!"

def test_logout_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"

    with patch.object(client.stub, 'Logout', return_value=server_pb2.StandardServerResponse(success=True, message="Logout Successful.")) as mock_logout:
        success, message = client.logout()

        assert success == True
        assert message == "Logout Successful."
        assert client.username == None
        mock_logout.assert_called_once_with(server_pb2.UserLogoutRequest(username="testuser"))

def test_logout_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"

    with patch.object(client.stub, 'Logout', return_value=server_pb2.StandardServerResponse(success=False, message="Logout failed.")) as mock_logout:
        success, message = client.logout()

        assert success == False
        assert message == "Logout failed."
        assert client.username == "testuser"
        mock_logout.assert_called_once_with(server_pb2.UserLogoutRequest(username="testuser"))

# def test_logout_server_error():
#     client = Client("127.0.0.1", 12345, "127.0.0.1")
#     client.username = "testuser"
    
#     with patch("client.client.write_socket") as mock_write_socket, \
#          patch("client.client.read_socket") as mock_read_socket:
        
#         mock_write_socket.return_value = None
#         mock_read_socket.return_value = None
        
#         success, message = client.logout()
        
#         assert success == False
#         assert message == "Server side error while attempting to logout. Please try again!"
#         assert client.username == "testuser"

def test_read_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"

    response = server_pb2.ReadMessageResponse()
    response.success.success = True
    response.success.message = "Messages found."
    message = response.success.messages.add()
    message.sender = "user1"
    message.timestamp = 1617184800
    message.message = "Hello!"
    
    with patch.object(client.stub, 'ReadMessages') as mock_read_messages:
        mock_read_messages.return_value = response
        
        success, messages = client.read(1)
        
        assert success == True
        assert messages == ["user1 at (03-31-2021, 06:00 AM): Hello!"]
        mock_read_messages.assert_called_once_with(server_pb2.ReadMessagesRequest(username="testuser", num_messages=1))

def test_read_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    response = server_pb2.ReadMessageResponse()
    response.failure.success = False
    response.failure.message = "No messages found."
    
    with patch.object(client.stub, 'ReadMessages') as mock_read_messages:
        mock_read_messages.return_value = response
        
        success, message = client.read(1)
        
        assert success == False
        assert message == "No messages found."
        mock_read_messages.assert_called_once_with(server_pb2.ReadMessagesRequest(username="testuser", num_messages=1))

# def test_read_server_error():
#     client = Client("127.0.0.1", 12345, "127.0.0.1")
#     client.username = "testuser"
    
#     with patch("client.client.write_socket") as mock_write_socket, \
#          patch("client.client.read_socket") as mock_read_socket:
        
#         mock_write_socket.return_value = None
#         mock_read_socket.return_value = None
        
#         success, message = client.read(1)
        
#         assert success == False
#         assert message == "Server side error while attempting to read messages. Please try again!"

def test_delete_account_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch.object(client.stub, 'DeleteAccount') as mock_delete_account:
        mock_delete_account.return_value = server_pb2.StandardServerResponse(success=True, message="Successfully deleted account!")
        
        success, message = client.delete_account()
        
        assert success == True
        assert message == "Successfully deleted account!"
        assert client.username == None
        mock_delete_account.assert_called_once_with(server_pb2.DeleteAccountRequest(username="testuser"))

def test_delete_account_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch.object(client.stub, 'DeleteAccount') as mock_delete_account:
        mock_delete_account.return_value = server_pb2.StandardServerResponse(success=False, message="Delete account failed.")
    
        success, message = client.delete_account()
    
        assert success == False
        assert message == "Delete account failed."
        assert client.username == "testuser"
        mock_delete_account.assert_called_once_with(server_pb2.DeleteAccountRequest(username="testuser"))

# def test_delete_account_server_error():
#     client = Client("127.0.0.1", 12345, "127.0.0.1")
#     client.username = "testuser"
    
#     with patch("client.client.write_socket") as mock_write_socket, \
#          patch("client.client.read_socket") as mock_read_socket:
        
#         mock_write_socket.return_value = None
#         mock_read_socket.return_value = None
        
#         success, message = client.delete_account()
        
#         assert success == False
#         assert message == "Server side error while attempting to delete account. Please try again!"
#         assert client.username == "testuser"

def test_fetch_sent_messages_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    response = server_pb2.FetchSentMessagesResponse()
    response.success.success = True
    response.success.message = "Sent messages fetched successfully."
    sent_message_1 = server_pb2.SentMessages(target_username="user1")
    sent_message_1.messages.add(sender="testuser", timestamp=1617184800, message="Message 1")
    sent_message_2 = server_pb2.SentMessages(target_username="user2")
    sent_message_2.messages.add(sender="testuser", timestamp=1617184801, message="Message 2")
    response.success.sent_messages.extend([sent_message_1, sent_message_2])
    
    with patch.object(client.stub, 'FetchSentMessages') as mock_fetch_sent_messages:
        mock_fetch_sent_messages.return_value = response
        
        success, sent_messages = client.fetch_sent_messages()
        
        assert success == True
        expected_messages = {
            "user1": [{"message": "Message 1", "message_id": '', "timestamp": 1617184800}],
            "user2": [{"message": "Message 2", "message_id": '', "timestamp": 1617184801}]
        }
        assert sent_messages == expected_messages
        mock_fetch_sent_messages.assert_called_once_with(server_pb2.FetchSentMessagesRequest(username="testuser"))

def test_fetch_sent_messages_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"

    response = server_pb2.FetchSentMessagesResponse()
    response.failure.success = False
    response.failure.message = "No sent messages found."

    with patch.object(client.stub, 'FetchSentMessages') as mock_fetch_sent_messages:
        mock_fetch_sent_messages.return_value = response
        success, message = client.fetch_sent_messages()
        assert success == False
        assert message == "No sent messages found."
        mock_fetch_sent_messages.assert_called_once_with(server_pb2.FetchSentMessagesRequest(username="testuser"))


# def test_fetch_sent_messages_server_error():
#     client = Client("127.0.0.1", 12345, "127.0.0.1")
#     client.username = "testuser"
    
#     with patch("client.client.write_socket") as mock_write_socket, \
#          patch("client.client.read_socket") as mock_read_socket:
        
#         mock_write_socket.return_value = None
#         mock_read_socket.return_value = None
        
#         success, message = client.fetch_sent_messages()
        
#         assert success == False

def test_delete_message_success():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch.object(client.stub, 'DeleteMessage') as mock_delete_message:
        mock_delete_message.return_value = server_pb2.StandardServerResponse(success=True, message="Message deleted successfully.")
        
        success, message = client.delete_message("1")
        
        assert success == True
        assert message == "Message deleted successfully."
        mock_delete_message.assert_called_once_with(server_pb2.DeleteMessageRequest(sender_username="testuser", message_id="1"))

def test_delete_message_failure():
    client = Client("127.0.0.1", 12345, "127.0.0.1")
    client.username = "testuser"
    
    with patch.object(client.stub, 'DeleteMessage') as mock_delete_message:
        mock_delete_message.return_value = server_pb2.StandardServerResponse(success=False, message="Delete message failed.")

        success, message = client.delete_message("1")

        assert success == False
        assert message == "Delete message failed."
        mock_delete_message.assert_called_once_with(server_pb2.DeleteMessageRequest(sender_username="testuser", message_id="1"))

# def test_delete_message_server_error():
#     client = Client("127.0.0.1", 12345, "127.0.0.1")
#     client.username = "testuser"
    
#     with patch("client.client.write_socket") as mock_write_socket, \
#          patch("client.client.read_socket") as mock_read_socket:
        
#         mock_write_socket.return_value = None
#         mock_read_socket.return_value = None
        
#         success, message = client.delete_message(1)
        
#         assert success == False
#         assert message == "Server side error while attempting to delete message. Please try again!"