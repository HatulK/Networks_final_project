from time import sleep

from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether
from scapy.layers.netflow import port
from scapy.sendrecv import sniff, send

client_ip = "192.168.1.100" # IP of the client sending the DNS request
dns_ip = "192.168.1.101"    # IP of the DNS server that will process the request
app_URL = "AmitOri.com"     # URL of the application server we want to find the IP of
app_server_ip = ""          # Placeholder for the application server's IP



def dns_packet_Handle(packet):
    global app_server_ip
    sleep(1)
    if IP in packet:
        # Extract source and destination IP addresses from the packet
        ip_source = packet[IP].src
        ip_dest = packet[IP].dst
        if packet.haslayer(DNS) and packet.haslayer(DNSRR):
            # Extract the URL that the DNS query is asking for
            app_server_URL = packet[DNSRR].rrname.decode().rstrip(".")
            if app_server_URL == app_URL:
                # If the requested URL matches our target, extract the IP address
                app_server_ip = packet[DNSRR].rdata

def get_app_server_ip():
    global app_server_ip
    return app_server_ip


def sendDNSRequest():
    ip = IP(src=client_ip, dst=dns_ip)  # fullfil       # IP packet header
    udp = UDP(sport=20247, dport=53)                    # UDP packet header (port 53 is for DNS)
    dnsqr = DNSQR(qname="AmitOri.com")                  # DNS query record
    dns = DNS(rd=1, qd=dnsqr)  # fullfil                # DNS packet
    packet = ip / udp / dns                             # Combine all headers to form the complete packet
    send(packet)                                        # Send the packet