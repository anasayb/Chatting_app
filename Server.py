# TODO: make the server send resived messages from one user to the other as a group chat

import socket
import threading

# Inizlizing the server info
PORT = 6060
SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())   # could result in probom when having multiple interfaces
ADDRESS = (SERVER_ADDRESS, PORT)

# Making the socket with the server info
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDRESS)

# Header is used to send the size of the message before sending the message
HEADER_SIZE = 64
FORMAT = "utf-8"

# Disconnect message
DISCONNECT = "!DISCONNECT!"

# This method handle the connection after accepting it in a seperate thread 
def client_handle(connection, clientAdress):
    client_Name, _, client_Adress = socket.gethostbyaddr(clientAdress[0])
    print(f"[NEW COONNECTION] {clientAdress} connected.")
    
    connected = True
    while connected:
        msg_length = connection.recv(HEADER_SIZE).decode(FORMAT)
        if msg_length:
            size = int(msg_length)
            msg = connection.recv(size).decode(FORMAT)
            
            if msg == DISCONNECT:
                connected = False

            print(f"[{client_Name}] {msg}")
    
    connection.close()

# This methodis used to start the lestining in the server
def start():
    SERVER.listen()
    print(f"Listenning on {SERVER_ADDRESS} ...")
    con = 0
    while True:
        connection, clientAddress = SERVER.accept()
        thread = threading.Thread(target= client_handle, args = (connection, clientAddress))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count()-1}")
        con += 1
        if con == 3:
            break


print("[STARTING] Server is starting...")
start()
print("[STOPING] The server is shutting down")