# Reliablee

This repository is an RDT implementation for the purposes of creating a protocol over TCP that, (a) does TCP pipelining at sender and receiver where multiple packet are in flight, (b) Sequence and acknowledgement numbers will be based on number of bytes transferred, (c) Fast re-transmit functionality

## Pipenv

To install `Pipenv`,

```bash
pip install pipenv
```

Using `Pipenv`,

```bash
pipenv shell
```

Updating `Pipfile` from a possible `requirements.txt`,

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

## Formatting The Repository

To format the repository use `autopep8` ( this comes in the dev of the `Pipfile`), run,

```bash
autopep8 -r . --in-place
```

## To Start

After doing,

```bash
pipenv shell && pipenv install
pipenv install --dev // if you would like to do development
```

Then just simply run,

```bash
pipenv run python app.py
```

## Brainstorming

### Class Based Representation

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

### Sender Vs Receiver

The only difference between either of them is who initiates the conversation first. A `Receiver` will always act in against of a `Sender`, anda `Sender` will always be the first one to initiate the conversation.

Thus, actually, both `Receiver` and `Sender` will act both as a `client` ( that makes some outgoing traffic and receives incoming traffic ), and a `server` ( that receives from incmoing traffic and prepares outgoing traffic ). Both almost sound the same, but it's important to focus on what happens firstly.

In the first step,

1. The `client` first creates some outgoing traffic, the `server` takes that as incomning traffic
2. The `server` does something with that incoming traffic, and sends an outgoing message back to the `client`.

You would think we would go for the usual paradigm of creating a normal socket and binding it to somewhere, then acting that in against to a server. But to me, at the moment, it seems like a better practice to create both a `client`, and a `server` in both of the processes that we will spin up, and both `listen` and `receive` on different ports.

As a consequence, I created separate ports for both the `Sender` and the `Receiver`.

An *easier* solution is to use a full duplex communication between `Sender` and `Receiver`, but I can't find any useful guides on how to achieve this using Python. Most leads show that *threading* will be used somewhere.

> Okay, nevermind, it's better to design this architecture as being async based transmission keeping in mind that I will have to start the clients and the servers on different ports in 2 different threads in each process. Wish me luck.

The above idea isn't bad, but true multithreading is not possible in Python. It's a language limitation due to the Python's Global Interpreter's Mutex Lock. Nevertheless, we can *implement* multithreading, even though the underlying mechanism isn't completely the same as in working with **C/C++**'s version of a library, say, **OpenMP**, or **MPI**. Please read the following extract for an explanation,

> "A thread is a separate flow of execution. This means that your program will have two things happening at once. But for most Python 3 implementations the different threads do not actually execute at the same time: they merely appear to.
>
> It’s tempting to think of threading as having two (or more) different processors running on your program, each one doing an independent task at the same time. That’s almost right. The threads may be running on different processors, but they will only be running one at a time.
>
> Getting multiple tasks running simultaneously requires a non-standard implementation of Python, writing some of your code in a different language, or using multiprocessing which comes with some extra overhead.
>
> Because of the way CPython implementation of Python works, threading may not speed up all tasks. This is due to interactions with the GIL that essentially limit one Python thread to run at a time." - [RealPython - An Intro to Threading in Python](https://realpython.com/intro-to-python-threading/)

## Reference

- [OmniSecu - Transmission Control Protocol (TCP) Segment Header, Transmission Control Protocol, TCP Header Fields](https://www.omnisecu.com/tcpip/tcp-header.php)
- [StackOverflow - How many characters can UTF-8 encode?](https://stackoverflow.com/questions/10229156/how-many-characters-can-utf-8-encode)
- [RealPython - Python Sockets](https://realpython.com/python-sockets/)
- [GitHub, sgtb3 - Reliable Data Transfer Protocol](https://github.com/sgtb3/Reliable-Data-Transfer-Protocol)
- [Github, Khouderchah Alex - libRDT](https://github.com/Khouderchah-Alex/libRDT)
- [YouTube, Ben Eater - TCP Connection Walkthrough](https://www.youtube.com/watch?v=F27PLin3TV0)
- [Python Docs - Socket Programming](https://docs.python.org/3/library/socket.html#socket.socket.settimeout)
- [Stack Exchange, Network Engineering - Why can't a single port be used for both incoming and outgoing traffic?](https://networkengineering.stackexchange.com/questions/33061/why-cant-a-single-port-be-used-for-both-incoming-and-outgoing-traffic)
- [RealPython - An Intro to Threading in Python](https://realpython.com/intro-to-python-threading/)
- [RealPython - Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/)
- [UTF8.com, UTF-8 and Unicode](https://www.utf8.com/#:~:text=It%20is%20an%20efficient%20encoding,character%20set%20on%20the%20Web.)
- [StackOverflow, Convert binary to ASCII and vice versa](https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa)
- [Pypi, autopep8](https://pypi.org/project/autopep8/)
- [Pypi, pipenv](https://pypi.org/project/pipenv/)