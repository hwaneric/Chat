import pytest
from unittest.mock import patch, mock_open
import json
import sys
import selectors
sys.path.append('../')
from server.account_management import load_user_data, save_user_data, username_exists, create_account

def test_load_user_data_file_exists():
    mock_data = {"testuser": {"password": "hashed_password"}}
    with patch("os.path.exists") as mock_exists, \
         patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        mock_exists.return_value = True
        result = load_user_data()
        assert result == mock_data

def test_load_user_data_file_not_exists():
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False
        result = load_user_data()
        assert result == {}

def test_save_user_data():
    users = {"testuser": {"password": "hashed_password"}}
    with patch("builtins.open", mock_open()) as mock_file:
        save_user_data(users)
        mock_file.assert_called_once_with("user_data.json", "w")
        handle = mock_file()
        handle.write.assert_any_call('{')
        handle.write.assert_any_call('"testuser"')
        handle.write.assert_any_call(': ')
        handle.write.assert_any_call('{')
        handle.write.assert_any_call('"password"')
        handle.write.assert_any_call(': ')
        handle.write.assert_any_call('"hashed_password"')
        handle.write.assert_any_call('}')
        handle.write.assert_any_call('}')

def test_username_exists_true():
    with patch('server.account_management.load_user_data') as mock_load_user_data:
        mock_load_user_data.return_value = {'testuser': {}}
        assert username_exists('testuser') == True

def test_username_exists_false():
    with patch('server.account_management.load_user_data') as mock_load_user_data:
        mock_load_user_data.return_value = {'anotheruser': {}}
        assert username_exists('testuser') == False

def test_username_exists_empty():
    with patch('server.account_management.load_user_data') as mock_load_user_data:
        mock_load_user_data.return_value = {}
        assert username_exists('testuser') == False

def test_create_account_success():
    dummy_users = {}
    with patch('server.account_management.load_user_data', return_value=dummy_users), \
         patch('server.account_management.save_user_data') as mock_save_user_data, \
         patch('server.account_management.username_exists', return_value=False), \
         patch('server.account_management.get_db_pathname', return_value='/mock/path'), \
         patch('builtins.open', mock_open()) as mock_file, \
         patch('bcrypt.hashpw', return_value=b'hashed_password'):
        
        result = create_account('testuser', 'password123', '127.0.0.1', 12345)
        
        assert result == {
            "success": True,
            "message": "Account created successfully.",
            "command": "server_response"
        }
        mock_save_user_data.assert_called_once_with({
            'testuser': {
                'username': 'testuser',
                'password': 'hashed_password',
                'online': True,
                'host': '127.0.0.1',
                'port': 12345
            }
        })
        mock_file.assert_called_once_with('/mock/path/unread_messages/testuser.json', 'w')
        mock_file().write.assert_called_once_with('[]')
