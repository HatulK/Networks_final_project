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
