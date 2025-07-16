#!/usr/bin/python3
"Calc checksum for all sniffed ICMP packages"
# Copyright (C) 2009-2021  David Villa Alises

import time
import socket
from string import printable

from inet_checksum import cksum


def nonprintable_to_dots():
    printable_bytes = printable.encode()[:-5]
    return bytes.join(b'', [bytes([c]) if c in printable_bytes else b'.'
                            for c in range(256)])

CHARMAP = nonprintable_to_dots()


def hexdump(frame, with_time=False):
    def to_chr(byteseq):
        retval = byteseq.translate(CHARMAP)
        return retval[:8] + b' ' + retval[8:]

    def to_hex(byteseq):
        retval = str.join(' ', ["%02X" % x for x in byteseq])
        return retval[:23] + ' ' + retval[23:]

    if with_time:
        print('--' + time.strftime("%H:%M:%s"))

    for i in range(0, len(frame), 16):
        line = frame[i:i + 16]
        print('%04X  %-49s |%-17s|' % (i, to_hex(line), to_chr(line).decode()))

    print()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                         socket.getprotobyname('icmp'))

    while 1:
        msg = sock.recv(1600)

        ihl = (msg[0] & 0x0F) * 4
        icmp = msg[ihl:]

        hexdump(icmp, True)

        if cksum(icmp[:]) != 0:
            print("Wrong ckecksum!!")


if __name__ == '__main__':
    main()
