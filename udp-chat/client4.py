#!/usr/bin/env python3
# Copyright: See AUTHORS and COPYING

import socket
from server4 import Chat

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = ('127.0.0.1', 12345)
Chat(sock, server).run()
