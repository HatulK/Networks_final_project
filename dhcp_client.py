from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

my_ip = ""
network = "enp0s3"
# Define the MAC address of the client
mac_str = uuid.getnode()
client_mac = ':'.join(['{:02x}'.format((mac_str >> i) & 0xff) for i in range(0, 48, 8)])


# Build the DHCP discover packet
def discover():
    dhcp_discover = Ether(dst='ff:ff:ff:ff:ff:ff', src=client_mac) / \
                    IP(src='0.0.0.0', dst='255.255.255.255') / \
                    UDP(sport=68, dport=67) / \
                    BOOTP(chaddr=client_mac, op=1) / \
                    DHCP(options=[('message-type', 'discover'),
                                  ('client_id', client_mac), ("requested_addr", "0.0.0.0"),
                                  ("option_list", [6, 3]),
                                  'end'])

    # Send the DHCP discover packet and capture the response
    sendp(dhcp_discover, iface=network)


def handle_dhcp(packet):
    time.sleep(1)
    ip = packet[BOOTP].yiaddr
    mac = packet[Ether].src
    # check if we got offer massage
    if DHCP in packet and packet[DHCP].options[0][1] == 2:
        print("--we got the offer--")

        # Create a DHCP request packet
        request_packet = Ether(dst="ff:ff:ff:ff:ff:ff", src=client_mac) / IP(src=ip, dst="255.255.255.255") / UDP(
            sport=68,
            dport=67) / BOOTP(
            op=1, chaddr=client_mac.replace(":", ""), xid=RandInt()) / DHCP(options=[("message-type", "request"),
                                                                                     ("requested_addr", ip),
                                                                                     ("server_id", "255.255.255.255"),
                                                                                     ("hostname", "client"), "end"])

        sendp(request_packet, iface=network)
    if DHCP in packet and packet[DHCP].options[0][1] == 5:
        print("----------ACK Received----------")
        my_ip = packet[BOOTP].yiaddr
        print(my_ip)