#!/usr/bin/env python3
# Copyright: See AUTHORS and COPYING

import socket
QUIT = 'bye'


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 12345))
    members = {}

    while 1:
        data, endpoint = sock.recvfrom(1024)
        message = data.decode()
        if endpoint not in members.keys():
            members[endpoint] = message
            print("User '{}' has joined the chat.".format(message))
            continue

        sender = members[endpoint]
        for member_endpoint, nick in members.items():
            if member_endpoint == endpoint:
                continue

            print(nick, '<-', message)
            encoded = "{}: {}".format(sender, message).encode()
            sock.sendto(encoded, member_endpoint)

        if message == QUIT:
            del members[endpoint]
            print("User '{}' has left the chat.".format(sender))


try:
    main()
except KeyboardInterrupt:
    print("shut down.")
