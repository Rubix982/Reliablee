#!/usr/bin/env python3

# Package imports
from dotenv import load_dotenv
import asyncio
import os

# Local imports
from controllers.ServerDriver import Servers
from controllers.ClientDriver import Clients

load_dotenv()

def main():

    if not os.path.exists('logs'):

        os.makedirs('logs')

        with open(str(os.environ['RECEIVER_LOG_FILENAME']), encoding='UTF-8', mode='w') as file:
            pass

        with open(str(os.environ['SENDER_LOG_FILENAME']), encoding='UTF-8', mode='w') as file:
            pass

    asyncio.run(Servers())
    asyncio.run(Clients())

    while True:
        pass

if __name__ == '__main__':
    main()