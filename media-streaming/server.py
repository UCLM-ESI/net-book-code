#!/usr/bin/env -S python -u

import sys
import socket
import time


def log(msg):
    sys.stderr.write(msg)
    sys.stderr.flush()


class Receiver:
    def __init__(self, port):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)
        self.sock.bind(('', port))
        self.sock.listen(1)

    def run(self):
        self.child, client = self.sock.accept()
        self.received = 0
        self.init = time.time()

        try:
            self.receiving()
        except KeyboardInterrupt:
            pass
        finally:
            self.sock.close()

    def receiving(self):
        while 1:
            data = self.child.recv(1024)
            if not data:
                break

            self.received += len(data)
            self.show_stats()

            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()

    def show_stats(self):
        elapsed = time.time() - self.init
        byterate = self.received / 1000 / elapsed
        bitrate = byterate * 8

        msg = f'received(kB):{self.received//1000:,}, '
        msg += f'rate(kBps):{byterate:,.0f}, '
        msg += f'rate(kbps):{bitrate:,.0f}'
        log(f'\r {msg} {10 * " "}\r')


port = int(sys.argv[1])
Receiver(port).run()
