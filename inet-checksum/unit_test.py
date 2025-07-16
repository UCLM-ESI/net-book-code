import struct
from unittest import TestCase

from inet_checksum import scapy_cksum, rfc_cksum
# from inet_checksum import scapy_cksum as cksum
# from inet_checksum import rfc_cksum as cksum
from inet_checksum import portable_cksum as cksum


class CheckSumTests(TestCase):
    def try_cksum(self, data, expected=b'\x00\x00'):
        data = bytes.fromhex(data)
        result = cksum(data).to_bytes(2, 'big')
        self.assertEqual(result, expected)

    def test_ip_header(self):
        self.try_cksum('45000073000040004011c0a80001c0a800c7', b'\xb8\x61')

    def test_ip_header_verify(self):
        self.try_cksum('45000073000040004011b861c0a80001c0a800c7', b'\x00\x00')

    def test_ip_header_notebook(self):
        data = bytes.fromhex('450000540000400040010000C0A80001C0A800C7')
        result = scapy_cksum(data).to_bytes(2, 'big')
        self.assertEqual(result, b'\xb8\x90')

    def test_ip_header_notebook_check(self):
        data = bytes.fromhex('450000540000400040010000C0A80001C0A800C7')
        result = scapy_cksum(data).to_bytes(2, 'big')
        self.assertEqual(result, b'\xb8\x90')

    def test_captured_icmp(self):
        data = '0800ddcb00f80013e707886000000000e6ed040000000000101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637'
        self.try_cksum(data, b'\x00\x00')

    def test_case_1(self):
        self.try_cksum('e34f2396442799f3', b'\x1a\xff')

    def test_case_2(self):
        self.try_cksum('9a560b8e0dcc', b'\x4c\x4f')

    def test_odd_1byte(self):
        data = b'\0\0\xaa'
        checksum = cksum(data)
        result = checksum.to_bytes(2, 'big') + data
        self.assertEqual(cksum(result), 0)

    def test_odd_3byte(self):
        data = b'\0\0\xaa\xbb\xcc'
        checksum = cksum(data)
        result = checksum.to_bytes(2, 'big') + data
        self.assertEqual(cksum(result), 0)

    def test_yap(self):
        header = b'YAP' + struct.pack('!HbH', 0, 0, 0)
        payload = b'f1e1adac-6ac4' + b'\0'
        checksum = cksum(header + payload)

        header = b'YAP' + struct.pack('!HbH', 0, 0, checksum)

        self.assertEqual(cksum(header + payload), 0)

    def test_yap2(self):
        data = b'YAP' + b'\x00\x00' + b'\0' + b'\x00\x00' + b'\x00\x01' + \
               b'NmE1OTg4MDktNTUwMS00ZjFiLTkxZjYtZTQxYjc2Zjc='
        first = cksum(data)

        first_b = struct.pack('!H', first)
        reply = b'YAP' + b'\x00\x00' + b'\0' + first_b + b'\x00\x01' + \
                b'NmE1OTg4MDktNTUwMS00ZjFiLTkxZjYtZTQxYjc2Zjc='
        verify = cksum(reply)

        self.assertEqual(verify, 0)

    def test_17bits_carry(self):
        size = 65538
        data = b'\xFF' * (size)
        checksum1 = scapy_cksum(data)
        checksum2 = rfc_cksum(data)
        self.assertEqual(checksum1, checksum2, f"Checksum mismatch {data.hex()}")
