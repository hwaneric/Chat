import pytest
from unittest.mock import patch, MagicMock, ANY
import time
import sys
import os
import threading
import grpc
from concurrent import futures
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../client')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../server')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../protos')))
from server import Server
from driver import initialize
from client import Client
import server_pb2
import server_pb2_grpc

@pytest.fixture(scope="module")
def start_servers():
    # Start servers in separate threads
    server_threads = []
    for server_id in range(3):
        thread = threading.Thread(target=initialize, args=(server_id, None), daemon=True)
        thread.start()
        server_threads.append(thread)
    
    # Allow some time for servers to start
    time.sleep(5)
    
    yield
    
    # Cleanup: stop servers
    for thread in server_threads:
        if thread.is_alive():
            thread.join()

def test_servers_connect(start_servers):
    # Connect to each server and verify connection
    server_stubs = []
    for server_id in range(3):
        host = f"127.0.0.1"
        port = 54400 + server_id
        channel = grpc.insecure_channel(f"{host}:{port}")
        stub = server_pb2_grpc.ServerStub(channel)
        server_stubs.append(stub)
    
    # Verify that each server is connected to the others
    for server_id, stub in enumerate(server_stubs):
        response = stub.CurrentLeader(server_pb2_grpc.CurrentLeaderRequest())
        assert response.leader == 0, f"Server {server_id} is not connected to the leader"

    print("All servers are successfully connected to each other.")