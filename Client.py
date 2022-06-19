# TODO: there is a problom that when ever recving a message the message will be displayed after the input promot, there are solutions but it requires the some sort of GUI implementaion (curses, tinker)
# TODO: use diffrente colors for diffrent users

import socket
import threading
from colorama import Fore, Style

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
    try:
        f = open("User_Info.txt")
        name = f.read()
    except FileNotFoundError:
        f = open("User_Info.txt", 'x')
        name = input("Please choose a name: ")
        f.write(name)       
    send(name) 
    thread = threading.Thread(target=recive)
    thread.start()


inizilize()
msg = ""
while msg != DISCONNECT:
    msg = input(f"[ YOU ] ")
    send(msg)
send(DISCONNECT)