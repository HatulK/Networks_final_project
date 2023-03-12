from time import sleep

from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether
from scapy.layers.netflow import port
from scapy.sendrecv import send, sniff

app_name = "AmitOri.com"
dns_ip = "192.168.1.101"
app_ip = "10.0.2.15"


def DNSPacketHandle(packet):
    sleep(1)
    if packet.haslayer(DNS):
        if packet.haslayer(DNSQR):
            req_name = packet[DNSQR].qname.decode().rstrip(".")
            if req_name == app_name:
                client_ip = packet[IP].src
                dnsrr = DNSRR(rrname=app_name, rdata=app_ip)
                ip = IP(src=dns_ip, dst=client_ip)  # fullfil
                udp = UDP(sport=53, dport=packet[UDP].sport)
                dns = DNS(id=packet[DNS].id, an=dnsrr, qr=1)  # fullfil
                packet = ip / udp / dns
                send(packet)


if __name__ == '__main__':
    print("DNS Server is running")
    sniff(filter="udp port 53", prn=DNSPacketHandle, iface="enp0s3")
