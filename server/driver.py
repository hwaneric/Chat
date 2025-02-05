import socket
import selectors
import types
from accept_wrapper import accept_wrapper
from service_conn import service_connection

sel = selectors.DefaultSelector()
HOST = "127.0.0.1"
PORT = 54400

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
          accept_wrapper(key.fileobj)
        else:
          service_connection(key, mask)
  except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
  finally:
    sel.close()
