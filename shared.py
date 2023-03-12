import socket

buffer=1024


def send_share(sock,data):
    offset = 0
    encoded_data=data.encode()       # convert the data to bytes
    while offset < len(encoded_data):
        chunk = encoded_data[offset:offset+buffer]       # split the data into chunks of the buffer size
        sent_bytes = sock.send(chunk)   # send the chunk
        offset += sent_bytes

# receive data in chunks
def receive_share(sock):
    received_data = b''     # initialize the received data as bytes
    while True:
        chunk = sock.recv(buffer)       # receive a chunk of data
        if not chunk:
            break
        received_data += chunk    # append the chunk to the received data
        if len(chunk) < buffer:     # if the chunk is smaller than the buffer size, it is the last chunk
            break
    return received_data.decode()   # convert the received data back to a string