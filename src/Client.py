#!/usr/bin/env python3

# Package imports
from dotenv import load_dotenv
import socket

# Local imports
from models.RDTReceiver import RDTReceiver
from models.RDTSender import RDTSender

load_dotenv()  # take environment variables from .env.

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello, world')
        data = s.recv(1024)

    print('Received', repr(data))

if __name__ == '__main__':
    main()