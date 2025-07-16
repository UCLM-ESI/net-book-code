#!/usr/bin/python3
"Internet checksum algorithm RFC-1071"
# from scapy:
# https://github.com/secdev/scapy/blob/master/scapy/utils.py

import sys
import struct
import array


def cksum(pkt):
    # type: (bytes) -> int
    if len(pkt) % 2 == 1:
        pkt += b'\0'
    s = sum(array.array('H', pkt))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    s = ~s

    if sys.byteorder == 'little':
        s = ((s >> 8) & 0xff) | s << 8

    return s & 0xffff


def cksum_good(header_bytes):
    assert len(header_bytes) % 2 == 0, "El tamaño debe ser par"

    checksum = 0
    for i in range(0, len(header_bytes), 2):
        word = (header_bytes[i] << 8) + header_bytes[i+1]
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    return ~checksum & 0xFFFF
