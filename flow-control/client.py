#!/usr/bin/env -S python -u
'Usage: client.py <host> <port>'

import sys
import socket
import time
import itertools

BLOCK = 10000 * b'x'

rotating = itertools.cycle('|/-\\')


def log(msg):
    sys.stderr.write(msg)
    sys.stderr.flush()


class Sender:
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        snd_buffer = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF) // 1000
        log(f'Sending buffer size: {snd_buffer:,} kB\n')

    def run(self):
        self.sent = 0
        self.init = time.time()

        try:
            self.sending()
        except KeyboardInterrupt:
            self.sock.close()

    def sending(self):
        while 1:
            self.show_stats()
            self.sent += self.sock.send(BLOCK)

    def show_stats(self):
        elapsed = time.time() - self.init
        msg = f'sent:{self.sent//1000:,} kB, '
        msg += f'rate:{self.sent/1000/elapsed:,.0f} kBps'
        log(f'\r ({next(rotating)}) {msg} {10 * " "}\r')
        time.sleep(0.01)


if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
Sender(host, port).run()
