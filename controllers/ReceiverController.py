#!/usr/bin/env python3

# Package imports
from dotenv import load_dotenv
import random
import socket
import time
import json
import os

# Local imports
from models.TCPPacket import TCPPacket
from models.AuxProcessing import AuxProcessing
from lib.GoBackN import GoBackNReceiver

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

# Go Back N Receiver Client
GoBackN = GoBackNReceiver()

# Data received
dataReceived = open(str(os.environ['MISC']), encoding='utf-8', mode='w')

def ReceiverClient():

    global TCPData, counter, GoBackN

    try:
        with open(str(os.environ['RECEIVER_LOG_FILENAME']), encoding='utf-8', mode='w') as PKTLogger:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

                # Bare ReceiverClient TCP config
                s.connect((HOST, CLIENT_PORT))
                TCPPkt = TCPPacket().ClientConfig()
                s.sendall(TCPPkt.EncodeObject())

                while True:
                    if TCPData == str(b'') or TCPData == None:
                        continue

                    TCPPkt = TCPPacket().CustomConfig(
                        **json.loads(TCPData[2:-1]))

                    PKTLogger.write(
                        f'[RECEIVED - {time.process_time()}] Counter: {counter} - {TCPPkt.__repr__()}\n{GoBackN.__repr__()}\n\n')
                    counter += 1

                    dataReceived.write(AuxProcessing.BinaryToUTF8(TCPPkt.data))

                    print(
                        f'[RECEIVER - {time.process_time()}] Received from Sender')

                    if str(os.environ['RECEIVER_DEBUG']) == 'True':
                        print('In Receiver Client', TCPPkt.__dict__)

                    # TCP Handshake, 3rd step
                    if TCPPkt.tcp_control_flags['SYN'] == 0x1 and \
                            TCPPkt.tcp_control_flags['ACK'] == 0x1 and \
                            GoBackN.ReceiveACK(TCPPkt):

                        # TCP Handshake, connection established
                        TCPPkt.tcp_control_flags['SYN'] = 0x0

                        '''
                        The receiver should only update the SEQ value
                        '''

                        TCPPkt.acknowledgement_number = AuxProcessing.IntegersToBinary(AuxProcessing.BinaryToIntegers(
                            TCPPkt.acknowledgement_number) + AuxProcessing.BinaryToIntegers(TCPPkt.sequence_number))

                    # Connection has already been established and we can now
                    # receive the information that we requested for
                    elif TCPPkt.tcp_control_flags['ACK'] == 0x1:

                        if GoBackN.ReceiveACK(TCPPkt):

                            TCPPkt.acknowledgement_number = TCPPkt.sequence_number

                            TCPPkt.sequence_number = AuxProcessing.IntegersToBinary(AuxProcessing.BinaryToIntegers(
                                TCPPkt.sequence_number) + len(AuxProcessing.BinaryToUTF8(TCPPkt.data)))

                        elif TCPPkt.acknowledgement_number == TCPPkt.sequence_number:
                            TCPPkt.sequence_number = AuxProcessing.IntegersToBinary(AuxProcessing.BinaryToIntegers(TCPPkt.sequence_number) + int(os.environ['DEFAULT_WINDOW_SIZE']))
                        else:

                            TCPPkt.acknowledgement_number = AuxProcessing.IntegersToBinary(
                                GoBackN.rcv_base)

                    # The end of the data is reached and the TCP
                    # connection can now be closed
                    elif TCPPkt.tcp_control_flags['FIN'] == 0x1:

                        PKTLogger.write(
                            f'[SENDING - {time.process_time()}] Counter: {counter} - {TCPPkt.__repr__()}\n{GoBackN.__repr__()}\n\n')
                        counter += 1

                        s.close()
                        PKTLogger.close()
                        dataReceived.close()
                        return

                    else:

                        raise Exception('Invalid TCP Packet Configuration')

                    PKTLogger.write(
                        f'[SENDING - {time.process_time()}] Counter: {counter} - {TCPPkt.__repr__()}\n{GoBackN.__repr__()}\n\n')
                    counter += 1

                    time.sleep(random.uniform(0.1, 0.8))

                    s.sendall(TCPPkt.EncodeObject())

                    TCPData = str(b'')

    except IOError as err:
        print("I/O error({0}): {1}".format(err.errno, err.strerror))


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
