import socket
import threading


PORT = 6060
SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER_ADDRESS, PORT)

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDRESS)

HEADER_SIZE = 64
FORMAT = "utf-8"

DISCONNECT = "!DISCONNECT!"

def client_handle(connection, clientAdress):
    print(f"[NEW COONNECTION] {clientAdress} connected.")
    
    connected = True
    while connected:
        msg_length = connection.recv(HEADER_SIZE).decode(FORMAT)
        if msg_length:
            size = int(msg_length)
            msg = connection.recv(size).decode(FORMAT)
            
            if msg == DISCONNECT:
                connected = False

            print(f"[{clientAdress}] {msg}")
    
    connection.close()


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