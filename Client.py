import socket
import threading
import time


SERVER_PORT = 6060
SERVER_ADDRESS = "192.168.1.185"
ADDRESS = (SERVER_ADDRESS, SERVER_PORT)

HEADER_SIZE = 64
FORMAT = "utf-8"

DISCONNECT = "!DISCONNECT!"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def send(message):
    msg_encoded = message.encode(FORMAT)
    msg_length = len(msg_encoded)
    length_encoded = str(msg_length).encode(FORMAT)
    length_encoded += b' ' * ( HEADER_SIZE - len(length_encoded))
    client.send(length_encoded)
    client.send(msg_encoded)

send("Hello world")
send(DISCONNECT)