# Reliablee

This repository is an RDT implementation for the purposes of creating a protocol over TCP that, (a) does TCP pipelining at sender and receiver where multiple packet are in flight, (b) Sequence and acknowledgement numbers will be based on number of bytes transferred, (c) Fast re-transmit functionality.

Some aspects are still partially incomplete as requirements were changed in the latter phase of the assignment.

## Pipenv

To install `Pipenv`,

```bash
pip install pipenv
```

Installing the dependencies,

```bash
pipenv install
```

Using `Pipenv`,

```bash
pipenv shell
```

## Formatting The Repository

To format the repository use `autopep8` ( this comes in the dev of the `Pipfile`), run,

```bash
autopep8 -r . --in-place
```

## To Start

After doing the setup, you can also run,

```bash
pipenv install --dev // if you would like to do development
```

Now, just run,

```bash
pipenv run python app.py
```

## Progress

'Cause you should make yourself feel better from time to time, no buts.

- [ ] Reliable Data Transfer [####################..............................]
- [ ] TCP Pipelinig [..................................................]
- [X] Sequence And Acknowledgement will be based on number of bytes transfered [##################################################]
- [ ] Fast Retransmit Functionality [..................................................]
- [ ] Proxy Server Configuration [##########..........................................]

*Note:* Each **#** is 5%

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

### RDT3.0 Data Loss

For context, take a look at `3.png`, `4.png` for the intent of doing only one TCP method at a single moment.

For the multipipelined approach to handling data loss, consider the `5.png`, `6.png`, `8.png`, `9.png`.

1. Considering the *only one TCP* at a single moment idea. Either it's,
   1. No loss
      1. We just dealt with it when we made a simple TCP Sender And Mechanism
   2. Packet Loss
      1. The only participant involved in this case is the Sender itself, which has an internal built in time for how long the packet has been out, and how long it should take for it to receive a response from the Receiver.
      2. In essence, all this is doing is starting a timer right after it **sends** the packet. It keeps checking if the timer has not exceeded some **fixed time out**. If it does, just send the packet again
   3. ACK Loss
      1. Two participants, but the catch 22 is that the receiver has no mechanism that says they should receive a packet within this time duration, thus all that in done in this scenario is again at the `Sender's` end, which is just resending the *pkt* if no *ACK* has been received for the last packet sent in a certain time duration
   4. Premature Timeout/Delayed ACK
      1. This needs an algorithm implementation. Time to study more.
      2. Okay so this can solved easily with the GoBackN algorithm

### Go-Back-N Algorithm

A Go-Back-N algorithm can be implemented with a Queue with a fixed size. We don't have to preallocate an entirely gigantic buffer. As a benefit of that, a queue can grow/shrink depending on the influx of traffic.

It's not practical to create a Go-Back-N buffer for each dedicated TCP. But if you create 1 Go-Back-N instance, and share it with all the clients sending requests to your server, it should be enough.

Also, a Go-Back-N will act on the client's side, not the server's side.

The next question is about what the individual entries of the Go-Back-N Algorithm will represent.

Its components consist of,

- A sender component
- A receiver component

For the sender component,

- A window size of length **N**
  - Window is of upto N, consecutive transmitted but unACKed pkts
  - k-bit seq# in pkt heaer
- A SendBase pointer, for the head of the queue
- A NextSeqNum pointer, for the first entry of 'usable, not yet sent'
- 4 different states,
  - Already ack'ed
  - Sent, not yet ack'ed
  - Usable, not yet sent
  - Not usable
- Timer for oldest in-flight packet
- Timeout(n): Retransmit packet n and all higher seq # packets in window

For the receiver component,

- ACK-only, always send ACK for correctly-received packet so far, with the highest in-order seq #
  - May generate duplcate ACKs
  - Need only remember rcv_base
- On receipt of out-of-order packet
  - Can discard (don't buffer) or buffer: an implementation decision
  - re-ACK pkt with highest in-order seq #
- Receiver view of sequence number space consists of the following states,
  - Received and ACKed
  - Out-of-order: Received but not ACKed
  - Not received

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
- [Docs Python, OpenSSL - Self-signed Certificates](https://docs.python.org/3.6/library/ssl.html#self-signed-certificates)
- [WhyNoHTTPS](https://whynohttps.com/)
- [GitHub, yh742 - Go Back N](https://github.com/yh742/go-back-n/)
