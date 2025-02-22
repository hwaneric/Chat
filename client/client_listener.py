import grpc
from concurrent import futures
import sys
sys.path.append('../')

import client_listener_pb2 as pb2
import client_listener_pb2_grpc as pb2_grpc

class Client_Listener(pb2_grpc.Client_ListenerServicer):
    def __init__(self, update_ui_callback):
        self.update_ui_callback = update_ui_callback

    def ReceiveOnlineMessage(self, request, context):
        sender = request.sender
        message = request.message

        display_text = f"\nNew message from {sender}: {message}"
        self.update_ui_callback(message)

        res = pb2.StandardServerResponse(success=True, message="Message received successfully")
        return res
    
