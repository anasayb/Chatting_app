# TODO: take input form the user then send
# TODO: allow the user to decide when to stop the connection


import socket

# Inizlizing the server info
SERVER_PORT = 6060
SERVER_ADDRESS = "192.168.1.185"
ADDRESS = (SERVER_ADDRESS, SERVER_PORT)

# Header is used to send the size of the message before sending the message
HEADER_SIZE = 64
FORMAT = "utf-8"

# Disconnect message
DISCONNECT = "!DISCONNECT!"

# Creating the client socket to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

# This method is used to send any text massge to the server
def send(message):
    msg_encoded = message.encode(FORMAT)
    msg_length = len(msg_encoded)
    length_encoded = str(msg_length).encode(FORMAT)
    length_encoded += b' ' * ( HEADER_SIZE - len(length_encoded))
    client.send(length_encoded)
    client.send(msg_encoded)

send("Hello world")
send(DISCONNECT)