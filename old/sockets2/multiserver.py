import socket
import threading

HOST = "localhost"

PORT = 9091

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)
        
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat'.encode("ascii"))
            nicknames.remove(nickname)
            break
            
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"{nickname} is {str(address)}")
        broadcast(f"{nickname} has joined the server".encode("ascii"))
        client.send("Connected to the server".encode("ascii"))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
        
        
receive()