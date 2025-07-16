#!/usr/bin/env python3

from inet_checksum import scapy_cksum, rfc_cksum, portable_cksum

data = [
    0x45, 0x00,
    0x00, 0x54,
    0x00, 0x00,
    0x40, 0x00,
    0x40, 0x01,
    0x00, 0x00,
    0xC0, 0xA8,
    0x00, 0x01,
    0xC0, 0xA8,
    0x00, 0xC7,
    0x10, 0x00
]


def my_cksum(data):
    remain = 0
    if len(data) % 2 == 1:
        remain = data.pop()

    checksum = 0
    for i in range(0, len(data), 2):
        tmp = (data[i] << 8) + data[i+1]
        checksum += tmp
        print(f"data[{i:2}:{i+1:2}]: 0x{tmp:04x}, cksum: {checksum:#4x}")

        if checksum >> 16:
            checksum = (checksum & 0xFFFF) + (checksum >> 16)
            print(f"  folding: {checksum:#4x}")

    if remain:
        checksum += remain << 8

    return ~checksum & 0xFFFF


print(hex(portable_cksum(bytes(data))))
