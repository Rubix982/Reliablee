class TCPControlFlags():

    def __init__(self):
        '''Control Bits govern the entire process of connection establishment, data transmissions and connection termination. The control bits are listed as follows, they are'''

        '''It indicates if we need to use Urgent pointer field or not. If it is set to 1 then only we use Urgent pointer.'''
        self.URG = 0x0

        '''It is set when an acknowledgement is being sent to the sender.'''
        self.ACK = 0x0

        '''When the bit is set, it tells the receiving TCP module to pass the data to the application immediately.'''
        self.PSH = 0x0

        '''When the bit is set, it aborts the connection. It is also used as a negative acknowledgement against a connection request.'''
        self.RST = 0x0

        '''It is used during the initial establishment of a connection. It is set when synchronizing process is initiated.'''
        self.SYN = 0x0

        '''The bit indicates that the host that sent the FIN bit has no more data to send.'''
        self.FIN = 0x0
