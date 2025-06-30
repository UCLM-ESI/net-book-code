#!/usr/bin/env python3
import socket
QUIT = 'bye'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 12345))
users = {}

while 1:
    data, endpoint = sock.recvfrom(1024)
    message = data.decode()
    if endpoint not in users.keys():
        users[endpoint] = message
        print("User '{}' has joined the chat.".format(message))
        continue

    for user_endpoint, nick in users.items():
        print(nick, user_endpoint, message)
        if user_endpoint != endpoint:
            message = "{}: {}".format(nick, message)
            sock.sendto(message.encode(), user_endpoint)

    if message == QUIT:
        del users[endpoint]
        print("User '{}' has left the chat.".format(endpoint))
