#!/usr/bin/env python3
"usage: %s [--server|--client]"

import sys
import socket
import selectors
SERVER = ('', 12345)
QUIT = b'bye'


class Chat:
    def __init__(self, sock, peer):
        self.sock = sock
        self.peer = peer

    def run(self):
        selector = selectors.DefaultSelector()
        selector.register(sys.stdin, selectors.EVENT_READ, self.sending)
        selector.register(self.sock, selectors.EVENT_READ, self.receiving)

        while 1:
            for key, mask in selector.select():
                if key.data(key.fileobj) == QUIT:
                    return

    def sending(self, fd):
        message = input().encode()
        self.sock.sendto(message, self.peer)
        return message

    def receiving(self, fd):
        message, _ = self.sock.recvfrom(1024)
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
        message, peer = sock.recvfrom(0, socket.MSG_PEEK)
    else:
        peer = SERVER

    Chat(sock, peer).run()
