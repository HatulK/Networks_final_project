# Create a DHCP offer packet
import time

from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

client_ip = "192.168.1.100"
server_ip = "192.168.1.1"
broad_cast = "255.255.255.255"

def handle_dhcp(packet):
    time.sleep(1)
    client_mac = packet[Ether].src
    server_mac = get_if_hwaddr("enp0s3")
    subnet_mask = "255.255.255.0"
    xid = packet[BOOTP].xid
    # Handle DHCP discovers from the client
    if DHCP in packet and packet[DHCP].options[0][1] == 1:

        print("i got discover --> sent a offer")
        offer_packet = Ether(dst=client_mac,src= get_if_hwaddr("enp0s3")) / IP(src=server_ip, dst=broad_cast) / UDP(sport=67, dport=68) / BOOTP(
            op=2, yiaddr=client_ip, siaddr=server_ip,chaddr=client_mac, xid=packet[BOOTP].xid) / DHCP(
            options=[("message-type", "offer"),
                     ("server_id", "192.168.1.1"), ("subnet_mask", "255.255.255.0"), ("router", server_ip),
                     ("lease_time", 86400), "end"])
        sendp(offer_packet)
    # Handle DHCP requests from the client
    elif DHCP in packet and packet[DHCP].options[0][1] == 3:
        print("i got a request ---> sent ack")
        # Create a DHCP acknowledge packet
        ack_packet = Ether(dst=client_mac) / IP(src=server_ip, dst=broad_cast) / UDP(sport=67,
                                                                                                    dport=68) / BOOTP(
            op=2, chaddr=client_mac, yiaddr=client_ip, siaddr=server_ip, xid=RandInt()) / DHCP(
            options=[("message-type", "ack"), ("server_id", server_ip), ("subnet_mask", "255.255.255.0"),
                     ("router", server_ip),
                     ("lease_time", 86400), "end"])

        # Send the DHCP acknowledge packet
        sendp(ack_packet, iface="enp0s3")

if __name__ == '__main__':
    print("DHCP Server is up \n")
    sniff(filter="udp and (port 67 or 68)", prn=handle_dhcp, iface="enp0s3")