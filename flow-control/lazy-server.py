#!/usr/bin/env -S python -u
'Usage: server.py <port>'

import sys
import socket


class Receiver:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        self.sock.listen(1)

    def run(self):
        self.conn, client = self.sock.accept()
        print(f'Client connected: {client}')

        rcv_buffer = self.conn.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF) // 1000
        print(f'Receiving buffer size: {rcv_buffer:,} kB')

        try:
            self.receiving()
        except KeyboardInterrupt:
            self.sock.close()

    def receiving(self):
        input('> ')
        while 1:
            received = 0
            for _ in range(100):
                data = self.conn.recv(5000)
                received += len(data)

            input(f'received: {received//1000:,} kB > ')


if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(1)

port = int(sys.argv[1])
Receiver(port).run()
