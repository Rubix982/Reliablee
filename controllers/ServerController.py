# Package imports
from socket import error as SocketError
from dotenv import load_dotenv
import requests
import urllib3
import os.path
import socket
import random
import errno
import os
import sys
import ssl

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Local imports
from src.LFU import LFUCache
from src.LRU import lrucache

load_dotenv()

def MainServerController():

    Proxy()

def Proxy():
    port_addr = (str(os.environ['HOSTNAME']), int(os.environ['PORT']))
    LFU_CACHE_SIZE, LRU_CACHE_SIZE = int(os.environ['LFU_CACHE_SIZE']), int(os.environ['LRU_CACHE_SIZE'])

    '''
    https://docs.python.org/3.6/library/ssl.html#ssl.Purpose.CLIENT_AUTH
    Purpose.CLIENT_AUTH loads CA certificates for client certificate verification on the server side.
    '''
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=str(os.environ['CERT_FILE']), keyfile=str(os.environ['KEY_FILE']))

    # Create a server socket, bind it to a port and start listening
    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSerSock.bind(port_addr)

    '''
    https://docs.python.org/3/library/socket.html#socket.socket.listen
    
    socket.listen([backlog])
    Enable a server to accept connections. If backlog is specified, it must be at least 0 (if it is lower, it is set to 0); it specifies the number of unaccepted connections that the system will allow before refusing new connections. If not specified, a default reasonable value is chosen.

    Changed in version 3.5: The backlog parameter is now optional    
    '''
    tcpSerSock.listen(40)

    while True:

        # Start receiving data from the client
        print(f'\nReady to serve at {port_addr}')
        tcpCliSock, addr = tcpSerSock.accept()

        # Throws HTTPS_PROXY_REQUEST error. I can't figure out why
        # tcpCliSock = context.wrap_socket(tcpCliSock)
        
        print('Received a connection from:', addr)
        message = tcpCliSock.recv(int(os.environ['BYTE_SIZE'])).decode('utf-8', 'ignore')

        if len(message.split(' ')) > 0:
            if message.split(' ')[1] == 'http://detectportal.firefox.com/success.txt' or message.split(' ')[1] == 'incoming.telemetry.mozilla.org:443':
                continue
        else:
            continue

        # Extract the filename from the given message
        if message.split(' ')[1].startswith('http') or message.split(' ')[1].startswith('https'):
            filename = message.split(' ')[1].split('//')[1]
        else:
            filename = message.split(':')[0].split(' ')[1]

        with open(str(os.environ['BLACKLIST_LOCATION']), mode='r') as file:
            for line in file:
                if filename == line[0:-1]:
                    print(
                        'This is one of the blocked domains. Forbidden 403!\r\n')
                    continue

        try:
            response = requests.get(f"https://{filename}", verify=False)
        except:
            print(f"Not found {filename}")
            continue

        # # START CACHING MECHANISM
        # CachingMechanism()
        # # END CACHING MECHANISM

        try:
            tcpCliSock.send(response.content + b"\r\n")
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                print(f'Connection Reset By Peer! {filename} ')
            continue
    tcpSerSock.shutdown(socket.SHUT_RDWR)
    tcpCliSock.close()

def CachingMechanism():
    lru_cache = lrucache(LRU_CACHE_SIZE)
    lfu_cache = LFUCache(LFU_CACHE_SIZE)

    # Check wether the file exist in the cache
    cache_file_path = f"cache/{filename}.{extension}"

    # Actual variable to store the data in
    response = None

    # # Checking if the data exists in the LFU cache
    if lfu_cache.get(filename) == -1:

        # Checking if the data exists in the LRU cache
        if lru_cache.get(filename) == None:

            # The data is neither in the LRU cache
            # and neither in the LFU cache

            # Thus, the answer is to receive data from the
            # origin server

            # Get the response from the origin server and
            # store it in the 'response' variable.
            # This is a requests object capable of including the
            # file headers and the content, both in type(str) and
            # type(bytes)
            response = requests.get(
                f"https://{filename}", verify=False)

        else:
            # This control flow means that the LRU cache contains
            # the desird key - the data exists in the LRU cache

            # Get the path of the lfu cache
            response_path = f'./cache/lru/{filename}.{extension}'

            # Variable to handle the storage of the received file data
            response = None

            # Reading and sending the received data from the file
            # to the variable 'data'
            with open(response_path, mode='r') as lru_file_path:
                data = lru_file_path.readlines()

            # Insert into the LFU Cache as well
            lfu_folder_size = len([name for name in os.listdir(
                './cache/lfu') if os.path.isfile(name)])

            # After getting the data from the folder
            # insert that data into the LFU cache as well

            # LFU folder cache size determination
            if lfu_folder_size < LFU_CACHE_SIZE:

                lfu_cache.put(filename, lfu_folder_size)

                # End of control flow for inserting data into the LFU cache

            else:
                # This control flow means that the LFU Folder is full
                # Till the desired capacity

                # Randomly pick a file from the './cache/lfu' folder
                file_to_delete = random.choice(
                    list(lfu_cache.node_for_key.values()))

                # Delete it in the folder
                os.remove(f'./cache/lfu/{file_to_delete}')

                # Remove the filename from the cache
                lfu_cache.node_for_key.pop(filename)

                # Set the lfu cache key to a value action
                lfu_cache.put(filename, lfu_folder_size)

                # Write to a file in the cache
                with open(f'./cache/lfu/{filename}.{extension}', mode='w') as lfu_file_path:
                    lfu_file_path.write(data)

                # End of else control flow for updating the LFU cache

            # End of if control flow for receiving data from the LRU cache

            lfu_path = f'./cache/lfu/{filename}.{extension}'

    else:

        # Start of control flow for getting the data from the LFU cache

        response_path = f'./cache/lfu/{filename}.{extension}'

        with open(response_path, mode='r') as lfu_file_path:
            data = lfu_file_path.readlines()

        # End of control flow for getting the data from the LFU Cache

    with open(cache_file_path, mode='w') as file:
        file.write(response.text)