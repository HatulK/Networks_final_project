import tcp_client
from tcp_client import *
from dns_client import *
from  dhcp_client import *

if __name__ == '__main__':
    # Get the MAC address of the client's interface
    mac_addr = get_if_hwaddr("enp0s3")
    print("MAC Address: "+ mac_addr)

    # DHCP
    discover()  # Send a DHCP discover packet to request an IP address lease
    # Sniff DHCP responses from the server and handle them
    sniff(filter="udp and (port 67 or 68)", prn=handle_dhcp, iface="enp0s3", count=3)

    # DNS
    sendDNSRequest()  # Send a DNS request packet to the DNS server
    # Sniff DNS responses from the server and handle them
    sniff(filter=f"udp port 53 and src {dns_ip}", count=1, timeout=5, prn=dns_packet_Handle, iface="enp0s3")
    print("App server IP is : " + get_app_server_ip())

    # TCP
    # Connect to the application server using TCP
    tcp_client.connect_client(get_app_server_ip())

