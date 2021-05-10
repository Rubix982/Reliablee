#!/usr/bin/env python3

# Package imports
from dotenv import load_dotenv
from socket

# Local imports
from models.TCPPacket import TCPPacket

load_dotenv()  # take environment variables from .env.

class RDTSender():

    def __init__(self):
        pass