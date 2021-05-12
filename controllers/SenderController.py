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

# take environment variables from .env
load_dotenv()

# The SENDER client's hostname or IP address
HOST = str(os.environ['HOST'])

# The port used by the SENDER client
CLIENT_PORT = int(os.environ['RECEIVER_PORT'])

# Port to listen on (non-privileged ports are > 1023)
SERVER_PORT = int(os.environ['SENDER_PORT'])

# Information to receive
BYTES_TO_RECEIVE = int(os.environ['BYTES_TO_RECEIVE'])

# Global data variable
TCPData = None

# Counter for interaction
counter = 0

# Data to send
data = ''

# Data index
data_index = 0


def SenderClient():

    global TCPData, counter, data, data_index

    with open(str(os.environ['DATA_TO_SEND']), mode='r') as file:
        data = file.read()

    with open(str(os.environ['SENDER_LOG_FILENAME']), mode='w') as file:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, CLIENT_PORT))

            while True:
                if TCPData == str(b'') or TCPData == None:
                    continue

                TCPPkt = TCPPacket().CustomConfig(**json.loads(TCPData[2:-1]))

                if str(os.environ['SENDER_DEBUG']) == 'True':
                    print('In Sender Client', TCPPkt.__dict__)

                # TCP Handshake, 1st step
                if TCPPkt.tcp_control_flags['SYN'] == 0x0 and TCPPkt.tcp_control_flags['ACK'] == 0x0:

                    # TCP Handshake, 2nd step
                    TCPPkt.tcp_control_flags['SYN'] = 0x1
                    TCPPkt.tcp_control_flags['ACK'] = 0x1

                    # The sender should only update the ACK value
                    TCPPkt.acknowledgement_number = AuxProcessing.IntegersToBinary(AuxProcessing.BinaryToIntegers(
                        TCPPkt.acknowledgement_number) + AuxProcessing.BinaryToIntegers(TCPPkt.sequence_number) + 1)

                # The connection has already been established
                elif TCPPkt.tcp_control_flags['ACK'] == 0x1:

                    # We have approached the end of the data
                    if data_index + int(os.environ['DEFAULT_WINDOW_SIZE']) >= len(data):

                        window_selected = data[data_index: data_index +
                                               (len(data) - data_index)]

                        # Set the FIN bit to 1
                        TCPPkt.tcp_control_flags['FIN'] = 0x1

                        # Set the ACK bit to 0
                        TCPPkt.tcp_control_flags['ACK'] = 0x0

                    else:

                        window_selected = data[data_index: data_index +
                                               int(os.environ['DEFAULT_WINDOW_SIZE'])]

                    __temp_store = TCPPkt.acknowledgement_number

                    TCPPkt.acknowledgement_number = AuxProcessing.IntegersToBinary(
                        AuxProcessing.BinaryToIntegers(TCPPkt.sequence_number) + len(window_selected))

                    TCPPkt.sequence_number = __temp_store

                    data_index = data_index + \
                        int(os.environ['DEFAULT_WINDOW_SIZE']) + 1

                    TCPPkt.data = AuxProcessing.UTF8ToBinary(window_selected)

                file.write(f'Counter: {counter} - {TCPPkt.__repr__()}\n')
                counter += 1

                time.sleep(0.25)

                s.sendall(TCPPkt.EncodeObject())

                TCPData = str(b'')


def SenderServer():

    global TCPData

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, SERVER_PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                TCPData = str(conn.recv(BYTES_TO_RECEIVE))
