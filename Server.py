# TODO: make the server send resived messages from one user to the other as a group chat

import socket
import threading

# This method is used to find the ip address of the server
def Find_IP_addess():
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        st.connect(('8.8.8.8',53))
        IP = st.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        st.close()
    return IP

# This method is used to inizilize the information of the client after establishing the connection
def inizilizeClient(connection):
    info ={}    
    msg_length = connection.recv(HEADER_SIZE).decode(FORMAT)
    if msg_length:
        size = int(msg_length)
        msg = connection.recv(size).decode(FORMAT)
        info["name"] = msg         
    return info

# This method handle the connection after accepting it in a seperate thread 
def client_handle(connection, clientAdress):

    info = inizilizeClient(connection)    
    print(f"[NEW COONNECTION] {clientAdress} connected.")

    connected = True
    while connected:
        msg_length = connection.recv(HEADER_SIZE).decode(FORMAT)
        if msg_length:
            size = int(msg_length)
            msg = connection.recv(size).decode(FORMAT)         
            if msg == DISCONNECT:
                connected = False
                print(f"[DISCONNECT] {info['name']} has disconnected!")
            else:
                print(f"[{info['name']}] {msg}")
    
    connection.close()

# This methodis used to start the lestining in the server
def start(SERVER):
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
       

# Making the socket
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Inizlizing the server info
SERVER_ADDRESS = Find_IP_addess()
PORT = 6060
ADDRESS = (SERVER_ADDRESS, PORT)
SERVER.bind(ADDRESS)

# Header is used to send the size of the message before sending the message
HEADER_SIZE = 64
FORMAT = "utf-8"

# Disconnect message
DISCONNECT = "!DISCONNECT!"


print("[STARTING] Server is starting...")
start(SERVER)
print("[STOPING] The server is shutting down")
SERVER.close()