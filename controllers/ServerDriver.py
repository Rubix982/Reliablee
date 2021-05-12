#!/usr/bin/env python3

# Package imports
import logging
import threading

# Local imports
from controllers.ReceiverController import ReceiverServer
from controllers.SenderController import SenderServer


async def Servers():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info('Main: Before ReceiverServer creating thread')
    thread_1 = threading.Thread(target=ReceiverServer, args=(), daemon=True)
    logging.info('Main: Before ReceiverServer running thread')

    thread_1.start()

    logging.info('Main: After ReceiverServer starting thread')

    logging.info('\n-------------\n')

    logging.info('Main: Before SenderServer creating thread')
    thread_2 = threading.Thread(target=SenderServer, args=(), daemon=True)
    logging.info('Main: Before SenderServer running thread')

    thread_2.start()

    logging.info('Main: After SenderServer starting thread')

    logging.info('\n-------------\n')
