#!/usr/bin/env python3

# Package imports
from dotenv import load_dotenv
from random import randrange
import os

# Local imports
from models.TCPControlFlags import TCPControlFlags
from models.AuxProcessing import AuxProcessing

load_dotenv() # take environment variables from .env

class TCPPacket:

    def __init__(self):
        '''Creates certain key variables for this structure'''

        '''16 Bit number which identifies the Source Port number (Sending Computer's TCP Port).'''        
        self.source_port = None

        '''16 Bit number which identifies the Destination Port number (Receiving Port).'''
        self.destination_port = None

        '''32 Bit number used for byte level numbering of TCP segments. If you are using TCP, each byte of data is assigned a sequence number. If SYN flag is set (during the initial three way handshake connection initiation), then this is the initial sequence number. The sequence number of the actual first data byte will then be this sequence number plus 1. For example, let the first byte of data by a device in a particular TCP header will have its sequence number in this field 50000. If this packet has 500 bytes of data in it, then the next packet sent by this device will have the sequence number of 50000 + 500 + 1 = 50501.'''
        self.sequence_number = None
        
        '''32 Bit number field which indicates the next sequence number that the sending device is expecting from the other device.'''
        self.acknowledgement_number = None

        '''4 Bit field which shows the number of 32 Bit words in the header. Also known as the Data Offset field. The minimum size header is 5 words (binary pattern is 0101).'''
        self.header_length = None

        '''Always set to 0 (Size 6 bits).'''
        self.reserved_bits = None

        '''We have seen before that TCP is a Connection Oriented Protocol. The meaning of Connection Oriented Protocol is that, before any data can be transmitted, a reliable connection must be obtained and acknowledged.'''
        self.tcp_control_flags = TCPControlFlags()

        '''Indicates the size of the receive window, which specifies the number of bytes beyond the sequence number in the acknowledgment field that the receiver is currently willing to receive.'''
        self.window = None

        '''The 16-bit checksum field is used for error-checking of the header and data'''
        self.checksum = None

        '''Shows the end of the urgent data so that interrupted data streams can continue. When the URG bit is set, the data is given priority over other data streams (Size 16 bits)'''
        self.urgent_pointer = None

        '''There can be up to 40 bytes of optional information in the TCP header'''
        self.optional_headers = {}

        '''The actual data'''
        self.data = None

    def ClientConfig(self):
        '''Initializes packet with default configuration for the client from the dotenv file'''
        
        '''Cient source port'''
        self.source_port = AuxProcessing.IntegersToBinary(int(os.environ['CLIENT_SENDER_PORT']))

        '''Destination port for the TCP Packet from the client - the server'''
        self.destination_port = AuxProcessing.IntegersToBinary(int(os.environ['SERVER_RECEIVER_PORT']))

        '''Setting the sequence number to start from 0'''
        self.sequence_number = AuxProcessing.IntegersToBinary(0)

        '''Acknowledgement Number'''
        self.acknowledgement_number = AuxProcessing.IntegersToBinary(0)

        '''Reserved bits to be set to zero'''
        self.reserved_bits = '0000'

        '''Control flags'''
        self.tcp_control_flags = TCPControlFlags()

        '''Window Size'''
        self.window = AuxProcessing.IntegersToBinary(int(os.environ['DEFAULT_WINDOW_SIZE']))

        '''Checksum value'''
        checksum_left_val = randrange(0, int(os.environ['CHECKSUM_VAL']))
        checksum_right_val = int(os.environ['CHECKSUM_VAL']) - checksum_left_val
        self.checksum = AuxProcessing.IntegersToBinary(checksum_left_val) + AuxProcessing.IntegersToBinary(checksum_right_val)

        '''Urgent pointer'''
        self.tcp_control_flags.URG = 0x0
        self.urgent_pointer = None

        '''Header size in word size, each word is 2 bytes ( 16 bits )'''
        self.header_length = AuxProcessing.IntegersToBinary(int(len(self.source_port + self.destination_port + self.sequence_number + self.acknowledgement_number + self.window + self.checksum) / 4) + len(self.reserved_bits) + len(self.tcp_control_flags.__dict__))

        '''Optional headers'''
        self.optional_headers = {}

        '''The actual data
        @TODO: I'm not going to handle this at
        the moment. The simplest idea is to use pinging
        as a technique to demonstrate how the RDT3.0 is working. So there is no actual data 
        transfer at the moment, only control transfer will be implemented at the moment'''
        self.data = None

        return self

    def ServerConfig(self):
        '''Initializes packet with default configuration for the server from the dotenv file'''
        
        '''Cient source port'''
        self.source_port = AuxProcessing.IntegersToBinary(int(os.environ['SERVER_SENDER_PORT']))

        '''Destination port for the TCP Packet from the client - the server'''
        self.destination_port = AuxProcessing.IntegersToBinary(int(os.environ['CLIENT_RECEIVER_PORT']))

        '''Setting the sequence number to start from 0'''
        self.sequence_number = AuxProcessing.IntegersToBinary(0)

        '''Acknowledgement Number'''
        self.acknowledgement_number = AuxProcessing.IntegersToBinary(0)

        '''Reserved bits to be set to zero'''
        self.reserved_bits = '00000'

        '''Control flags'''
        self.tcp_control_flags = TCPControlFlags()

        '''Window Size'''
        self.window = AuxProcessing.IntegersToBinary(int(os.environ['DEFAULT_WINDOW_SIZE']))

        '''Checksum value'''
        checksum_left_val = randrange(0, int(os.environ['CHECKSUM_VAL']))
        checksum_right_val = int(os.environ['CHECKSUM_VAL']) - checksum_left_val
        self.checksum = AuxProcessing.IntegersToBinary(checksum_left_val) + AuxProcessing.IntegersToBinary(checksum_right_val)

        '''Urgent pointer'''
        self.tcp_control_flags.URG = 0x0
        self.urgent_pointer = None

        '''Header size in word size, each word is 2 bytes ( 16 bits )'''
        self.header_length = AuxProcessing.IntegersToBinary(int(len(self.source_port + self.destination_port + self.sequence_number + self.acknowledgement_number + self.window + self.checksum) / 4) + len(self.reserved_bits) + len(self.tcp_control_flags.__dict__))

        '''Optional headers'''
        self.optional_headers = {}

        '''The actual data
        @TODO: I'm not going to handle this at
        the moment. The simplest idea is to use pinging
        as a technique to demonstrate how the RDT3.0 is working. So there is no actual data 
        transfer at the moment, only control transfer will be implemented at the moment'''
        self.data = None

        return self        