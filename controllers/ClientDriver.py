#!/usr/bin/env python3

# Package imports
import logging
import threading

# Local imports
from controllers.ReceiverController import ReceiverClient
from controllers.SenderController import SenderClient


async def Clients():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info('Main: Before ReceiverClient creating thread')
    thread_1 = threading.Thread(target=ReceiverClient, args=(), daemon=True)
    logging.info('Main: Before ReceiverClient running thread')

    thread_1.start()

    logging.info('Main: After ReceiverClient starting thread')

    logging.info('\n-------------\n')

    logging.info('Main: Before SenderClient creating thread')
    thread_2 = threading.Thread(target=SenderClient, args=(), daemon=True)
    logging.info('Main: Before SenderClient running thread')

    thread_2.start()

    logging.info('Main: After SenderClient starting thread')

    logging.info('\n-------------\n')
