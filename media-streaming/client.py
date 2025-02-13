#!/usr/bin/env -S python -u
'Usage: client.py <host> <port>'

import sys
import socket
import time


def log(msg):
    sys.stderr.write(msg)
    sys.stderr.flush()


class Sender:
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)

    def run(self):
        self.sent = 0
        self.init = time.time()

        try:
            self.sending()
        except KeyboardInterrupt:
            pass
        finally:
            self.sock.close()

    def sending(self):
        while 1:
            data = sys.stdin.buffer.read(1024)
            if not data:
                break

            self.sent += self.sock.send(data)
            self.show_stats()

    def show_stats(self):
        elapsed = time.time() - self.init
        byterate = self.sent / elapsed / 1000
        bitrate = byterate * 8

        msg = f'sent(kB):{self.sent//1000:,}, '
        msg += f'rate(kBps):{byterate:,.0f}, '
        msg += f'rate(kbps):{bitrate:,.0f}'
        log(f'\r {msg} {10 * " "}\r')


if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
Sender(host, port).run()
