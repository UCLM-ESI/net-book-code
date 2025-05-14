#!/usr/bin/env python3
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import socket
from server4 import Chat

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = ('127.0.0.1', 12345)
Chat(sock, server).run()
