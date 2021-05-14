#!/usr/bin/env python3

# Package imports
from dotenv import load_dotenv
from enum import Enum
import os

# Local imports
from models.TCPPacket import TCPPacket
from models.AuxProcessing import AuxProcessing

# Loads .env file
load_dotenv()


class SenderWindow(Enum):
    SENT = 1
    USABLE = 2
    ACK = 3


class GoBackNReceiver:

    def __init__(self):

        # This represents the acknowledgement number
        # that the receiver expects from the sender
        self.rcv_base = 0
        self.firstPKT = True

    def ReceiveACK(self, TCPPkt: TCPPacket):

        if self.firstPKT:
            self.firstPKT = False
            self.rcv_base = 1

        elif self.rcv_base + int(os.environ['DEFAULT_WINDOW_SIZE']) == AuxProcessing.BinaryToIntegers(TCPPkt.sequence_number):
            self.UpdateReceiveBase()
            return True

        else:
            return False

    def UpdateReceiveBase(self):
        self.rcv_base += int(os.environ['DEFAULT_WINDOW_SIZE'])

    def __repr__(self):
        return f"RCV_Base: {self.rcv_base}"


class GoBackNSender:

    def __init__(self, size: int = 1024, window: list = []):
        self.size = size
        self.window = window
        self.ptrNextSeqNum = -1

    def InsertEntry(self, ACK: int, COLOR: int):

        if len(self.window) + 1 > self.size:
            raise Exception('Size limit reached for GBN-Sender')

        if self.ptrNextSeqNum == -1 and COLOR == SenderWindow.USABLE:
            self.ptrNextSeqNum = len(self.window)

        if COLOR == SenderWindow.USABLE:
            self.window.append({'ACK': ACK, 'COLOR': COLOR, 'COUNT': 0})

        if COLOR == SenderWindow.SENT:
            self.window.insert(self.ptrNextSeq, {
                               'ACK': ACK, 'COLOR': COLOR, 'COUNT': 0})

    def ReceiveACK(self, TCP: TCPPacket):

        # SEQ = AuxProcessing.BinaryToIntegers(TCP.sequence_number)
        SEQ = AuxProcessing.BinaryToIntegers(TCP.acknowledgement_number)

        if len(self.window) == 0:
            raise Exception('Window is of size zero')

        if self.window[0]['ACK'] == SEQ:
            self.window.pop(0)
            self.ptrNextSeqNum -= 1
            return True

        for entry in self.window:
            if entry['ACK'] == SEQ:
                entry['COUNT'] += 1

        return False

    def SendPkt(self):

        if len(self.window) == 0 and self.ptrNextSeqNum == 0:
            return

        if self.ptrNextSeqNum > len(self.window):
            # No packets left to send
            return False

        # Change the color is available
        self.window[self.ptrNextSeqNum]['COLOR'] = SenderWindow.SENT

        # Increment index
        self.ptrNextSeqNum += 1

        # Return True
        return True

    def __repr__(self):
        return f'Size: {self.size}, Window: {self.window}, PTRNextSeqNum: {self.ptrNextSeqNum}'

    def __str__(self):
        entries = []
        for entry in self.window:
            entries.append(entry)

        return entries
