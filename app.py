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

        with open(str(os.environ['RECEIVER_LOG_FILENAME']), encoding='UTF-8', mode='w') as ReceiverPKTLog, \
            open(str(os.environ['SENDER_LOG_FILENAME']), encoding='UTF-8', mode='w') as SenderPKTLog, \
                open(str(os.environ['RECEIVER_LOG_LOGGER']), encoding='UTF-8', mode='w') as ReceiverStreamLogger, \
        open(str(os.environ['SENDER_LOG_LOGGER']), encoding='UTF-8', mode='w') as SenderStreamLogger, \
            open(str(os.environ['MISC']), encoding='UTF-8', mode='w') as Misc:
            pass

    asyncio.run(Servers())
    asyncio.run(Clients())

    while True:
        pass


if __name__ == '__main__':
    main()
