# TODO: make the program only ask the user for the name in the first time running the program

from pydoc import cli
import socket
import threading

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
try:
    client.connect(ADDRESS)
except Exception:
    print("Sorry the server is not Online (Sadge)\nPlease try again later.")
    exit()

# This method is used to send any text massge to the server
def send(message):
    msg_encoded = message.encode(FORMAT)
    msg_length = len(msg_encoded)
    length_encoded = str(msg_length).encode(FORMAT)
    length_encoded += b' ' * ( HEADER_SIZE - len(length_encoded))
    client.send(length_encoded)
    client.send(msg_encoded)

# This method is used to recive other clients messge from the server
def recive():
    while True:
        msg_length = client.recv(HEADER_SIZE).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT:
                print("you have been disconnected.")
                return
            else:
                print(msg)
        



# This method is used to inizilize the information between client and server after creating the connection
def inizilize():
    name = input("Please choose a name: ")
    send(name)
    thread = threading.Thread(target=recive)
    thread.start()


inizilize()
msg = ""
while msg != DISCONNECT:
    msg = input(f"[ YOU ] ")
    send(msg)
send(DISCONNECT)