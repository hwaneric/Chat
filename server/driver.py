from concurrent import futures
import time
import grpc
import sys
from server import Server
sys.path.append('../protos')
import server_pb2 
import server_pb2_grpc
import client_listener_pb2
import client_listener_pb2_grpc
from account_management import check_if_online, create_account, fetch_sent_messages, list_accounts, login, logout, logout_all_users, read_messages, send_offline_message, delete_account, delete_message
import threading

from dotenv import load_dotenv
import os
load_dotenv()
HOST = os.getenv("SERVER_HOST")
PORT = int(os.getenv("SERVER_PORT"))

def serve(server_object):
    '''
        Starts the server and listens for incoming requests
    '''

    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_pb2_grpc.add_ServerServicer_to_server(server_object, server)
        address = f"{server_object.host}:{server_object.port}"
        server.add_insecure_port(address)
        server.start()
        print(f"Running server on host: {server_object.host} and port: {server_object.port}")
        server.wait_for_termination()

    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
        logout_all_users(server_object.db_path)

def connect(server_object):
    '''
        Connects to other servers in the cluster
    '''
    print("Attempting to Connect to other servers")

    # Create a channel to connect to other servers
    for i in range(3):
        if i == server_object.id:
            continue

        host = os.getenv(f"SERVER_HOST_{i}")
        port = int(os.getenv(f"SERVER_PORT_{i}"))

        MAX_RETRIES = 20
        retry_delay = 2  # seconds

        # Attempt to connect to the server of client {id}
        for attempt in range(MAX_RETRIES):
            try:
                channel = grpc.insecure_channel(f"{host}:{port}")
                grpc.channel_ready_future(channel).result(timeout=retry_delay)
                # channel = grpc.insecure_channel(f"{host}:{port}")
                stub = server_pb2_grpc.ServerStub(channel)
                server_object.server_stubs[i] = stub
                    
            except grpc.FutureTimeoutError:
                # Connection Attempt Timed Out
                if attempt == MAX_RETRIES - 1:
                    print(f"Failed to connect to server {i} after {MAX_RETRIES} attempts.")
                    break

                time.sleep(retry_delay)

        print(f"Connected to server {i}")
    
    print("Connected to all servers")
    
        

def initialize(id, db_path):
    print("host and port", f"SERVER_HOST_{id}", f"SERVER_PORT_{id}")
    host, port = os.getenv(f"SERVER_HOST_{id}"), int(os.getenv(f"SERVER_PORT_{id}"))
    server_object = Server(id, host, port, db_path)

    # Set Server 0 As Leader
    if id == 0:
        server_object.is_leader = True
        print("Server is leader")
    else:
        print("Server is not leader")

    # Connect to other servers in background thread
    threading.Thread(target=connect, args=(server_object,), daemon=True).start()

    serve(server_object)
    server_object.cleanup()




if __name__ == '__main__':
    # serve()
    if len(sys.argv) < 2:
        print("Usage: python driver.py <server_id> <optional: db_path>")
        sys.exit(1)
    
    # Get command line arguments
    server_id = sys.argv[1]
    db_path = None
    if len(sys.argv) == 3:
        db_path = sys.argv[2]

    # Validate Command Line Arguments
    if not server_id.isdigit():
        print("Invalid server ID. Server ID must be an integer.")
        sys.exit(1)

    server_id = int(server_id)
    if server_id not in [0, 1, 2]:
        print("Invalid server ID. Please provide 0, 1, or 2.")
        sys.exit(1)

    initialize(server_id, db_path)
