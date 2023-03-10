import socket

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set a port number
port = 12345

# connect to the server
client_socket.connect((host, port))
print(f"Connected to server {host} on port {port}")

# send data to the server
message = "Hello, server!"
client_socket.sendall(message.encode('utf-8'))
print(f"Sent message: {message}")

# receive data from the server
data = client_socket.recv(1024)
print(f"Received response: {data.decode('utf-8')}")

# close the connection
client_socket.close()
print("Connection closed")

import socket

# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
sock.connect(server_address)

# send a message to the server
message = 'transfer_player\nLionel Messi\nPSG\n'
sock.sendall(message.encode())

# receive the response from the server
data = sock.recv(1024)

# print the response
print(data.decode())

# close the socket
sock.close()
