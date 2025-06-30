#!/usr/bin/env python3
# Copyright: See AUTHORS and COPYING

import socket
from server4 import Chat, server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Chat(sock, server).run()
