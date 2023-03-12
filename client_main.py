import tcp_client
from tcp_client import *
from dns_client import *
from  dhcp_client import *
if __name__ == '__main__':
    mac_addr = get_if_hwaddr("enp0s3")

    print("MAC Address: "+ mac_addr)
    #DHCP
    discover()
    sniff(filter="udp and (port 67 or 68)", prn=handle_dhcp, iface="enp0s3", count=3)
    #DNS
    sendDNSRequest()  # Sending a DNS packet request
    sniff(filter=f"udp port 53 and src {dns_ip}", count=1, timeout=5, prn=dns_packet_Handle,
          iface="enp0s3")  # Sniffing the requested answer
    print("App server IP is : " + get_app_server_ip())
    #TCP
    tcp_client.connect_client(get_app_server_ip())
