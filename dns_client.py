from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether
from scapy.layers.netflow import port
from scapy.sendrecv import sniff, send

client_ip = "192.168.1.100"
dns_ip = "192.168.1.101"
app_URL = "AmitOri.com"
app_server_ip = ""


def dns_packet_Handle(packet):
    global app_server_ip
    if IP in packet:
        ip_source = packet[IP].src
        ip_dest = packet[IP].dst
        if packet.haslayer(DNS) and packet.haslayer(DNSRR):
            app_server_URL = packet[DNSRR].rrname.decode().rstrip(".")
            if app_server_URL == app_URL:
                app_server_ip = packet[DNSRR].rdata


def sendDNSRequest():
    ip = IP(src=client_ip, dst=dns_ip)  # fullfil
    udp = UDP(sport=20247, dport=53)
    dnsqr = DNSQR(qname="AmitOri.com")
    dns = DNS(rd=1, qd=dnsqr)  # fullfil
    packet = ip / udp / dns
    send(packet)


if __name__ == '__main__':
    sendDNSRequest()  # Sending a DNS packet request
    sniff(filter=f"udp port 53 and src {dns_ip}", count=1, timeout=5, prn=dns_packet_Handle,
          iface="enp0s3")  # Sniffing the requested answer
    print("App server IP is : " + app_server_ip)
