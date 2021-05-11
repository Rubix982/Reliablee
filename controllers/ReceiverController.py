#!/usr/bin/env python3

# Package imports
from dotenv import load_dotenv
import socket
import os

# take environment variables from .env.
load_dotenv()  

# Standard loopback interface address (localhost)
HOST = str(os.environ['HOST']) 

# The port used by the receiver client
CLIENT_PORT = int(os.environ['SENDER_PORT'])        

# Port to listen on (non-privileged ports are > 1023)
SERVER_PORT = int(os.environ['RECEIVER_PORT'])

# Information to receive
BYTES_TO_RECEIVE = int(os.environ['BYTES_TO_RECEIVE'])

def ReceiverClient():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, CLIENT_PORT))
        s.sendall(b'Hello, world')
        data = s.recv(BYTES_TO_RECEIVE)

    print('Received', repr(data))

def ReceiverServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, SERVER_PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(BYTES_TO_RECEIVE)
                if not data:
                    break
                conn.sendall(data)