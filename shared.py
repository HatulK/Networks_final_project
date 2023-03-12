import socket

buffer=1024


def send_share(sock,data):
    offset = 0
    encoded_data=data.encode()
    while offset < len(encoded_data):
        chunk = encoded_data[offset:offset+buffer]
        sent_bytes = sock.send(chunk)
        offset += sent_bytes

# receive data in chunks
def receive_share(sock):
    received_data = b''
    while True:
        chunk = sock.recv(buffer)
        if not chunk:
            break
        received_data += chunk
        if len(chunk) < buffer:
            break
    return received_data.decode()