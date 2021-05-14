#!/usr/bin/env python3

# Package imports
from enum import Enum


class SenderWindow(Enum):
    SENT = 1
    USABLE = 2


class GoBackNReceiver:

    def __init__(self):
        self.rcv_base = 0

    def ReceiveACK(self, ACK: int):
        return self.rcv_base == ACK

    def UpdateReceiveBase(self, ACK: int):
        self.rcv_base = ACK


class GoBackNSender:

    def __init__(self, size: int = 1024, window: list = []):
        self.size = size
        self.window = window
        self.ptrNextSeqNum = -1

    def InsertSent(self, ACK: int, COLOR: int):

        if len(self.window) + 1 > self.size:
            raise Exception('Size limit reached for GBN-Sender')

        if self.ptrNextSeqNum == -1 and COLOR == SenderWindow.USABLE:
            self.ptrNextSeqNum = len(self.window)

        if COLOR == SenderWindow.USABLE:
            self.window.append({'ACK': ACK, 'COLOR': COLOR, 'COUNT': 0})

        if COLOR == SenderWindow.SENT:
            self.window.insert(self.ptrNextSeq, {
                               'ACK': ACK, 'COLOR': COLOR, 'COUNT': 0})

    def ReceiveACK(self, ACK: int):

        if len(self.window) == 0:
            raise Exception('Window is of size zero')

        if self.window[0].ACK == ACK:
            self.window.pop(0)
            return True

        for entry in self.window:
            if entry.ACK == ACK:
                entry.COUNT += 1

        return False

    def SendPkt(self):

        if self.ptrNextSeqNum > len(self.window):
            # No packets left to send
            return False

        # Change the color is available
        self.window[self.ptrNextSeqNum]['COLOR'] = SenderWindow.SENT

        # Increment index
        self.ptrNextSeqNum += 1

        # Return True
        return True
