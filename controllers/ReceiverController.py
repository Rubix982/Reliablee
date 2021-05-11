#!/usr/bin/env python3

# Package imports
from dotenv import load_dotenv
import socket
import time
import json
import os

# Local imports
from models.TCPPacket import TCPPacket
from models.AuxProcessing import AuxProcessing

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

# Global data variable
TCPData = None

# Counter for interaction
counter = 0

def ReceiverClient():

    global TCPData, counter

    with open(str(os.environ['RECEIVER_LOG_FILENAME']), mode='w') as file:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # Bare ReceiverClient TCP config
            s.connect((HOST, CLIENT_PORT))
            TCPPkt = TCPPacket().ClientConfig()
            s.sendall(TCPPkt.EncodeObject())

            while True:
                if TCPData == str(b'') or TCPData == None:
                    continue

                TCPPkt = TCPPacket().CustomConfig(**json.loads(TCPData[2:-1]))

                print('In Receiver Client', TCPPkt.__dict__)

                if TCPPkt.tcp_control_flags['SYN'] == 0x0:
                    TCPPkt.tcp_control_flags['SYN'] = 0x1

                if TCPPkt.tcp_control_flags['ACK'] == 0x0:
                    TCPPkt.tcp_control_flags['ACK'] = 0x1

                TCPPkt.sequence_number = AuxProcessing.IntegersToBinary(AuxProcessing.BinaryToIntegers(TCPPkt.sequence_number) + AuxProcessing.BinaryToIntegers(TCPPkt.acknowledgement_number))

                file.write(f'Counter: {counter} - {TCPPkt.__repr__}\n')
                counter += 1

                time.sleep(0.75)

                s.sendall(TCPPkt.EncodeObject())

def ReceiverServer():

    global TCPData

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, SERVER_PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                TCPData = str(conn.recv(BYTES_TO_RECEIVE))