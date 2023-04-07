import socket
import threading
import os
import sys
import time
HOST = "localhost"

PORT = 9091

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []
nicknames = []

def sendback(client, message):
    client.send(message.encode("ascii"))
    
def commands(client, message):
    print(f"{nicknames[clients.index(client)]} used command: [{message}]")
    if message.startswith("!time"):
        message2 = time.strftime("%H:%M:%S", time.localtime())
        sendback(client, message2)
    
    
    
    else:
        message2 = "INVALID COMMAND | type !help for command list"
        sendback(client, message2)
def broadcast(message, client2):
    for client in clients:
        client.send(f"{nicknames[clients.index(client2)]}: {message}".encode("ascii"))
        
def startLeave(message):
    for client in clients:
        client.send(f"{message}".encode("ascii"))

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode("ascii").startswith(f"!"):
                commands(client, message.decode("ascii"))
                #sendback(client)
            else:
                broadcast(message.decode("ascii"), client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            startLeave(f'{nickname} has left the chat')
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
        startLeave(f"{nickname} has joined the server")
        client.send("Connected to the server".encode("ascii"))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
        
def type1():
    while True:
        ep = input("")
        if ep =="exit1":
            print("hello")
            sys.exit()

type_thread = threading.Thread(target=type1)
type_thread.start()
receive()