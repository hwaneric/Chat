import socket
import selectors
import types
from accept_wrapper import accept_wrapper
from account_management import logout_all_users
from service_conn import service_connection
from dotenv import load_dotenv
import os

load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

sel = selectors.DefaultSelector()
print("hostname:", socket.gethostbyname(socket.gethostname()))

if __name__ == "__main__":
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print("Listening on", (HOST, PORT))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)
    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(sel, key.fileobj)
                else:
                    service_connection(sel, key, mask)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        logout_all_users()
        sel.close()

