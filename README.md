# Reliablee

This repository is an RDT implementation for the purposes of creating a protocol over TCP that, (a) does TCP pipelining at sender and receiver where multiple packet are in flight, (b) Sequence and acknowledgement numbers will be based on number of bytes transferred, (c) Fast re-transmit functionality

## Pipenv

Using `Pipenv`,

```bash
pipenv shell
```

Updating `Pipfile`,

```bash
pipenv install -r requirements.txt
```

Updating `Pipfile.lock`,

```bash
pipenv lock --pre --clear
```

Installing a package,

```bash
pipenv install [package_name]
```

## Brainstorming

Each state in the RDT3.0 module represents two things,

1. What action was taken
2. What to respond with

In the end, it will be TCP packets that will be passed to and from the client and the server. Thus, it makes sense to allocate the representation of that to a TCP Packet class. Each state in both the RDT figures deal with either the,

1. Receiver
2. Sender

responsibility, either one of them, or both. Thus, our overall representation consists of two individual combinations of,

1. States
2. Receivers And Senders

It makes sense to make the sender act as `Client` since it makes the first move. Then we have to make the receiver act as `Server`, since it it works on an event trigger.

We can now thus,

1. Create separate `Client` and `Server` files
2. Create clases to represent the `RDTSender`, and `RDTReceiver`. Both of these will exist inside of the `Client`, and `Server` files
3. Inside of the `RDTSender`, and the `RDTReceiver` classes, we can say that we can use the `TCP` set of classes to encoding and decoding the binary packet representation of the TCP header segment. See `assets/2.png` for further context

## Reference

- [OmniSecu - Transmission Control Protocol (TCP) Segment Header, Transmission Control Protocol, TCP Header Fields](https://www.omnisecu.com/tcpip/tcp-header.php)
- [StackOverflow - How many characters can UTF-8 encode?](https://stackoverflow.com/questions/10229156/how-many-characters-can-utf-8-encode)
- [RealPython - Python Sockets](https://realpython.com/python-sockets/)
- [GitHub, sgtb3 - Reliable Data Transfer Protocol](https://github.com/sgtb3/Reliable-Data-Transfer-Protocol)
- [Github, Khouderchah Alex - libRDT ](https://github.com/Khouderchah-Alex/libRDT)
- [YouTube, Ben Eater - TCP Connection Walkthrough](https://www.youtube.com/watch?v=F27PLin3TV0)
- [Python Docs - Socket Programming](https://docs.python.org/3/library/socket.html#socket.socket.settimeout)

