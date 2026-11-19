
import socket
import os
import struct
from ctypes import *


# host to listen on
host = "192.168.193.129"


# our IP header
class IP(Structure):
    _pack_ = 1

    _fields_ = [
        ("version", c_ubyte, 4),
        ("ihl", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_uint32),
        ("dst", c_uint32)
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):

        self.protocol_map = {
            1: "ICMP",
            6: "TCP",
            17: "UDP"
        }

        # human readable IP addresses
        self.src_address = socket.inet_ntoa(socket_buffer[12:16])
        self.dst_address = socket.inet_ntoa(socket_buffer[16:20])

        # human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except KeyError:
            self.protocol = str(self.protocol_num)


# create raw socket
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(
    socket.AF_INET,
    socket.SOCK_RAW,
    socket_protocol
)

sniffer.bind((host, 0))

sniffer.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_HDRINCL,
    1
)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:

        # read packet
        raw_buffer = sniffer.recvfrom(65565)[0]

        # decode IP header
        ip_header = IP(raw_buffer[0:20])

        # display information
        print(
            "Protocol: {} {} -> {}".format(
                ip_header.protocol,
                ip_header.src_address,
                ip_header.dst_address
            )
        )

except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

finally:
    sniffer.close()
