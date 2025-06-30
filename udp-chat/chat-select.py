#!/usr/bin/env python3
# Copyright: See AUTHORS and COPYING

"usage: %s [--server|--client]"

import sys
import socket
from select import select
SERVER = ('', 12345)
QUIT = b'bye'


class Chat:
    def __init__(self, sock, peer):
        self.sock = sock
        self.peer = peer

    def run(self):
        fds = [sys.stdin, self.sock]
        while 1:
            ready = select(fds, [], [])[0]
            for fd in ready:
                if self.sock in ready:
                    msg = self.receiving()
                else:
                    msg = self.sending()

                if msg == QUIT:
                    return

    def sending(self):
        message = input().encode()
        self.sock.sendto(message, self.peer)
        return message

    def receiving(self):
        message, peer = self.sock.recvfrom(1024)
        print("other> {}".format(message.decode()))
        return message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__ % sys.argv[0])
        sys.exit()

    mode = sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if mode == '--server':
        sock.bind(SERVER)
        message, client = sock.recvfrom(0, socket.MSG_PEEK)
        Chat(sock, client).run()

    else:
        Chat(sock, SERVER).run()
