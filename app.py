#!/usr/bin/env python3

# Package imports
import asyncio

# Local imports
from controllers.ServerDriver import Servers
from controllers.ClientDriver import Clients

def main():
    asyncio.run(Servers())
    asyncio.run(Clients())

    while True:
        pass

if __name__ == '__main__':
    main()