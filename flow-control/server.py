#!/usr/bin/env -S python -u
'Usage: server.py <port> <rx_limit_limit>'

import sys
import socket
import time


def log(msg):
    sys.stderr.write(msg)
    sys.stderr.flush()


class Receiver:
    def __init__(self, port, rate_limit):
        self.rate_limit = rate_limit * 10**3
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        self.sock.listen(1)

    def run(self):
        self.conn, client = self.sock.accept()
        print(f'Client connected: {client}')

        rcv_buffer = self.conn.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF) // 1000
        log(f'Receiving buffer size: {rcv_buffer:,} kB\n')

        self.init = time.time()
        self.received = 0

        try:
            self.receiving()
        except KeyboardInterrupt:
            self.sock.close()

    def receiving(self):
        while 1:
            data = self.conn.recv(4096)
            if not data:
                break

            self.received += len(data)
            elapsed = time.time() - self.init
            self.current_rate = self.received / elapsed
            self.show_stats()

            if self.current_rate <= self.rate_limit:
                continue

            sleep_time = (self.received / self.rate_limit) - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def show_stats(self):
        msg = f'received:{self.received//1000:,} kB, '
        msg += f'rate:{self.current_rate/1000:,.0f} kBps'
        log(f'\r {msg} {10 * " "}\r')


if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(1)

port = int(sys.argv[1])
limit = int(sys.argv[2])
Receiver(port, limit).run()
