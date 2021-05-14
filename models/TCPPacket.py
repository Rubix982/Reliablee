#!/usr/bin/env python3

# Package imports
from dotenv import load_dotenv
from random import randrange
import json
import os

# Local imports
from models.TCPControlFlags import TCPControlFlags
from models.AuxProcessing import AuxProcessing

load_dotenv()  # take environment variables from .env


class TCPPacket:

    def __init__(self, source_port: str = 16 * '0', destination_port: str = 16 * '0',
                 sequence_number: str = 32 * '0', acknowledgement_number: str = 16 * '0', header_length: str = 4 * '0', reserved_bits: str = 6 * '0', tcp_control_flags: TCPControlFlags = TCPControlFlags(), window: str = 16 * '0', checksum: str = 16 * '0', urgent_pointer: str = 16 * '0', optional_headers: dict = {}, data: str = 4 * '0'):
        '''Creates certain key variables for this structure'''

        '''16 Bit number which identifies the Source Port number (Sending Computer's TCP Port).'''
        self.source_port = source_port

        '''16 Bit number which identifies the Destination Port number (Receiving Port).'''
        self.destination_port = destination_port

        '''32 Bit number used for byte level numbering of TCP segments. If you are using TCP, each byte of data is assigned a sequence number. If SYN flag is set (during the initial three way handshake connection initiation), then this is the initial sequence number. The sequence number of the actual first data byte will then be this sequence number plus 1. For example, let the first byte of data by a device in a particular TCP header will have its sequence number in this field 50000. If this packet has 500 bytes of data in it, then the next packet sent by this device will have the sequence number of 50000 + 500 + 1 = 50501.'''
        self.sequence_number = sequence_number

        '''32 Bit number field which indicates the next sequence number that the sending device is expecting from the other device.'''
        self.acknowledgement_number = acknowledgement_number

        '''4 Bit field which shows the number of 32 Bit words in the header. Also known as the Data Offset field. The minimum size header is 5 words (binary pattern is 0101).'''
        self.header_length = header_length

        '''Always set to 0 (Size 6 bits).'''
        self.reserved_bits = reserved_bits

        '''We have seen before that TCP is a Connection Oriented Protocol. The meaning of Connection Oriented Protocol is that, before any data can be transmitted, a reliable connection must be obtained and acknowledged.'''
        self.tcp_control_flags = tcp_control_flags.__dict__

        '''Indicates the size of the receive window, which specifies the number of bytes beyond the sequence number in the acknowledgment field that the receiver is currently willing to receive.'''
        self.window = window

        '''The 16-bit checksum field is used for error-checking of the header and data'''
        self.checksum = checksum

        '''Shows the end of the urgent data so that interrupted data streams can continue. When the URG bit is set, the data is given priority over other data streams (Size 16 bits)'''
        self.urgent_pointer = urgent_pointer

        '''There can be up to 40 bytes of optional information in the TCP header'''
        self.optional_headers = optional_headers

        '''The actual data'''
        self.data = data

    def ClientConfig(self):
        '''Initializes packet with default configuration for the client from the dotenv file'''

        '''Cient source port'''
        self.source_port = AuxProcessing.IntegersToBinary(
            int(os.environ['SENDER_PORT']))
        self.source_port = ((16 - len(self.source_port))
                            * '0') + self.source_port

        '''Destination port for the TCP Packet from the client - the server'''
        self.destination_port = AuxProcessing.IntegersToBinary(
            int(os.environ['RECEIVER_PORT']))
        self.destination_port = (
            (16 - len(self.destination_port)) * '0') + self.destination_port

        '''Setting the sequence number to start from 0'''
        self.sequence_number = AuxProcessing.IntegersToBinary(0)
        self.sequence_number = (
            (32 - len(self.sequence_number)) * '0') + self.sequence_number

        '''Acknowledgement Number'''
        self.acknowledgement_number = AuxProcessing.IntegersToBinary(0)
        self.acknowledgement_number = (
            (32 - len(self.acknowledgement_number)) * '0') + self.acknowledgement_number

        '''Reserved bits to be set to zero'''
        self.reserved_bits = '000000'

        '''Control flags'''
        self.tcp_control_flags = TCPControlFlags().__dict__

        '''Window Size'''
        self.window = AuxProcessing.IntegersToBinary(
            int(os.environ['DEFAULT_WINDOW_SIZE']))
        self.window = ((16 - len(self.window)) * '0') + self.window

        '''Checksum value'''
        checksum_left_val = randrange(0, int(os.environ['CHECKSUM_VAL']))
        checksum_right_val = int(
            os.environ['CHECKSUM_VAL']) - checksum_left_val
        self.checksum = AuxProcessing.IntegersToBinary(
            checksum_left_val) + AuxProcessing.IntegersToBinary(checksum_right_val)

        '''Urgent pointer'''
        self.tcp_control_flags['URG'] = 0x0
        self.urgent_pointer = 16 * '0'

        '''Header size in word size, each word is 2 bytes ( 16 bits )'''
        self.header_length = AuxProcessing.IntegersToBinary(int(len(self.source_port + self.destination_port + self.sequence_number +
                                                                    self.acknowledgement_number + self.window + self.checksum) / 4) + len(self.reserved_bits) + len(self.tcp_control_flags))
        self.header_length = ((16 - len(self.header_length))
                              * '0') + self.header_length

        '''Optional headers'''
        self.optional_headers = {}

        '''The actual data
        @TODO: I'm not going to handle this at
        the moment. The simplest idea is to use pinging
        as a technique to demonstrate how the RDT3.0 is working. So there is no actual data 
        transfer at the moment, only control transfer will be implemented at the moment'''
        self.data = AuxProcessing.UTF8ToBinary('.')

        return self

    def ServerConfig(self):
        '''Initializes packet with default configuration for the server from the dotenv file'''

        '''Cient source port'''
        self.source_port = AuxProcessing.IntegersToBinary(
            int(os.environ['RECEIVER_PORT']))
        self.source_port = ((16 - len(self.source_port))
                            * '0') + self.source_port

        '''Destination port for the TCP Packet from the client - the server'''
        self.destination_port = AuxProcessing.IntegersToBinary(
            int(os.environ['SENDER_PORT']))
        self.destination_port = (
            (16 - len(self.destination_port)) * '0') + self.destination_port

        '''Setting the sequence number to start from 0'''
        self.sequence_number = AuxProcessing.IntegersToBinary(0)
        self.sequence_number = (
            (32 - len(self.sequence_number)) * '0') + self.sequence_number

        '''Acknowledgement Number'''
        self.acknowledgement_number = AuxProcessing.IntegersToBinary(0)
        self.acknowledgement_number = (
            (32 - len(self.acknowledgement_number)) * '0') + self.acknowledgement_number

        '''Reserved bits to be set to zero'''
        self.reserved_bits = '000000'

        '''Control flags'''
        self.tcp_control_flags = TCPControlFlags().__dict__

        '''Window Size'''
        self.window = AuxProcessing.IntegersToBinary(
            int(os.environ['DEFAULT_WINDOW_SIZE']))
        self.window = ((16 - len(self.window)) * '0') + self.window

        '''Checksum value'''
        checksum_left_val = randrange(0, int(os.environ['CHECKSUM_VAL']))
        checksum_right_val = int(
            os.environ['CHECKSUM_VAL']) - checksum_left_val
        self.checksum = AuxProcessing.IntegersToBinary(
            checksum_left_val) + AuxProcessing.IntegersToBinary(checksum_right_val)

        '''Urgent pointer'''
        self.tcp_control_flags['URG'] = 0x0
        self.urgent_pointer = 16 * '0'

        '''Header size in word size, each word is 2 bytes ( 16 bits )'''
        self.header_length = AuxProcessing.IntegersToBinary(int(len(self.source_port + self.destination_port + self.sequence_number +
                                                                    self.acknowledgement_number + self.window + self.checksum) / 4) + len(self.reserved_bits) + len(self.tcp_control_flags))
        self.header_length = ((16 - len(self.header_length))
                              * '0') + self.header_length

        '''Optional headers'''
        self.optional_headers = {}

        '''The actual data
        @TODO: I'm not going to handle this at
        the moment. The simplest idea is to use pinging
        as a technique to demonstrate how the RDT3.0 is working. So there is no actual data 
        transfer at the moment, only control transfer will be implemented at the moment'''
        self.data = AuxProcessing.UTF8ToBinary('.')

        return self

    def CustomConfig(self, **kwargs):
        '''Initializes packet with default configuration for the client from the dotenv file'''

        '''Cient source port'''
        self.source_port = kwargs['source_port']

        '''Destination port for the TCP Packet from the client - the server'''
        self.destination_port = kwargs['destination_port']

        '''Setting the sequence number to start from 0'''
        self.sequence_number = kwargs['sequence_number']

        '''Acknowledgement Number'''
        self.acknowledgement_number = kwargs['acknowledgement_number']

        '''Reserved bits to be set to zero'''
        self.reserved_bits = kwargs['reserved_bits']

        '''Control flags'''
        self.tcp_control_flags = kwargs['tcp_control_flags']

        '''Window Size'''
        self.window = kwargs['window']

        '''Checksum value'''
        self.checksum = kwargs['checksum']

        '''Urgent pointer'''
        self.urgent_pointer = kwargs['urgent_pointer']

        '''Header size in word size, each word is 2 bytes ( 16 bits )'''
        self.header_length = kwargs['header_length']

        '''Optional headers'''
        self.optional_headers = kwargs['optional_headers']

        '''The actual data
        @TODO: I'm not going to handle this at
        the moment. The simplest idea is to use pinging
        as a technique to demonstrate how the RDT3.0 is working. So there is no actual data 
        transfer at the moment, only control transfer will be implemented at the moment'''
        self.data = kwargs['data']

        return self

    def ConvertToBinary(self):

        binRepresentation = ''

        for key, item in self.__dict__.items():
            print(key, item)
            if key == 'tcp_control_flags':
                for _, value in self.__dict__[key].__dict__.items():
                    binRepresentation += str(value)
            elif key == 'optional_headers':
                for _, value in self.__dict__[key].items():
                    binRepresentation += value
            elif key != 'data':
                binRepresentation += (item)

        return binRepresentation

    def EncodeObject(self):

        return json.dumps(self.__dict__).encode('UTF-8')

    def __repr__(self, isData: bool = False):
        return f"Source: {AuxProcessing.BinaryToIntegers(self.source_port)}, Destination: {AuxProcessing.BinaryToIntegers(self.destination_port)}, Sequence: {AuxProcessing.BinaryToIntegers(self.sequence_number)}, Acknowledgement: {AuxProcessing.BinaryToIntegers(self.acknowledgement_number)}, TCP Control Flags: {self.tcp_control_flags}, Checksum: {AuxProcessing.BinaryToIntegers(self.checksum)}, Optional Headers: {self.optional_headers} { f', Data: {AuxProcessing.BinaryToUTF8(self.data)}' if isData else ''}"
