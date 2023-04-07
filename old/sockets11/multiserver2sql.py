import socket
import threading
import os
import sys
import time
import datetime
from multiprocessing import Process
import sqlqueries
sqlqueries.printhello()
connection = sqlqueries.serverConnect(" [SQL server ip]", "test", "test", "chatroom")
yes = sqlqueries.accountCheck(connection, "victor@gmail.com")
print(yes)
yes2 = sqlqueries.historyAdd(connection,"34", 'qwerqwrwqer')
print(yes2)


print("start server-------------------")
#HOST = "localhost"
#PORT = 9091
#server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.bind((HOST,PORT))
#server.listen()

#HOST = "localhost"
#PORT = 9092
#server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server2.bind((HOST,PORT))
#server2.listen()
id_socket = {}
clients = []
nicknames = []
thread_id = []

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

def handle(client, PORT, HOST):
    #run login check the add id and scoket to the dictionary. Then remove on disconnect. Determin what to do if exitsts already.
    #id_socket["color"] = "red"
    #print(id_socket)
    while True:
        try:
            message = client.recv(1024)
            print(PORT ,message.decode("ascii"), nicknames)
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
            
def receive(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen()
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)
        
        
        client.send("EMAIL".encode("ascii"))
        email = client.recv(1024).decode("ascii")
        client.send("PASSWORD".encode("ascii"))
        password = client.recv(1024).decode("ascii")
        sqlqueries.loginSystem(connection, email, password)
        ######why is there two diffrent spellings of connection?
        
        print(f"{nickname} is {str(address)}")
        startLeave(f"{nickname} has joined the server")
        client.send("Connected to the server".encode("ascii"))
        print(client)
        print("--------------------------")
        print(address)
        thread = threading.Thread(target=handle, args=(client,PORT, HOST))
        thread.setDaemon(True)
        thread.start()
        thread_id.append(thread)
        print(thread_id)
        
def type1():
    while True:
        ep = input("")
        if ep =="exit1":
            print("hello")
            for i in thread_id:
                print(i.isDaemon())
            os._exit(1)
            exit()

type_thread = threading.Thread(target=type1)
type_thread.setDaemon(True)
type_thread.start()
thread_id.append(type_thread)
print(thread_id)

#if __name__ == '__main__':
#    p = Process(target=receive, args=('localhost',9091,))
#    p.start()
#    p2 = Process(target=receive, args=('localhost',9092,))
#    p2.start()
   
 

receive("localhost", 9091)

#def worker(d, key, value):
#    d[key] = value
#each thread can store the clients username/id. this would solve several problem
#each thread must go through a login function to make sure you are you
#the sets the username/id/others to a varible in the thread
#an error made was returning the clients in that one function
#a better way would be to return the socket.socket connecitons i need
#this is the only information i need to send the information to the other clients in the room.