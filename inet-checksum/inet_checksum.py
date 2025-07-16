#!/usr/bin/python3
"Internet checksum algorithm RFC-1071"
# from scapy:
# https://github.com/secdev/scapy/blob/0f7b0c0db7507b5af1c2e26e30668c8c976ea643/scapy/utils.py#L595

import sys
import array


def scapy_cksum(pkt: bytes) -> int:
    if len(pkt) % 2 == 1:
        pkt += b'\0'  # little endian only

    s = sum(array.array('H', pkt))  # native byte order
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    s = ~s

    if sys.byteorder == 'little':
        s = ((s >> 8) & 0xff) | s << 8

    return s & 0xffff


def rfc_cksum(data: bytes) -> int:
    if len(data) % 2 == 1:
        data += b'\0'  # little endian only

    total = sum(array.array('H', data))   # native byte order

    while (total >> 16):
        total = (total >> 16) + (total & 0xffff)

    if sys.byteorder == 'little':
        total = ((total >> 8) & 0xff) | total << 8

    return ~total & 0xffff


def portable_cksum(data: bytes) -> int:
    if len(data) % 2 == 1:
        data += b'\0'

    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) + data[i+1]  # big endian
        total = (total & 0xffff) + (total >> 16)

    return ~total & 0xffff


cksum = rfc_cksum
