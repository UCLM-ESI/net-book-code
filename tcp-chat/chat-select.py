#!/usr/bin/env python3
# Copyright: See AUTHORS and COPYING
"usage: %s [--server|--client]"

import sys
import socket
from select import select

SERVER = ('localhost', 12345)
QUIT = 'bye\n'


class Chat:
    def __init__(self, sock):
        self.sock = sock
        self.file = sock.makefile('r')
        self.running = True

    def run(self):
        while self.running:
            ready = select([sys.stdin, self.sock], [], [])[0]
            for fd in ready:
                if fd == self.sock:
                    msg = self.receiving()
                else:
                    msg = self.sending()

    def sending(self):
        message = sys.stdin.readline()
        self.sock.sendall(message.encode())
        if message == QUIT:
            self.running = False

    def receiving(self):
        message = self.file.readline()
        print("other> {}".format(message.strip()))
        if message in [QUIT, '']:
            self.running = False


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__ % sys.argv[0])
        sys.exit()

    mode = sys.argv[1]
    sock = socket.socket()

    if mode == '--server':
        sock.bind(SERVER)
        sock.listen(1)
        conn, addr = sock.accept()
        Chat(conn).run()
        conn.close()
    else:
        sock.connect(SERVER)
        Chat(sock).run()

    sock.close()
