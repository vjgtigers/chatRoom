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
sqlqueries.onStart(connection) # runs a set of commands on start


#remove print statements from room change

print("start server-------------------")

id_socket = {}
id_socket_client = {}
class User_id:
    def __init__(self, name, email, id1, sockConn):
        self.name = name   
        self.email = email
        self.id1 = id1
        self.socket = sockConn


thread_id = []

def sendback(clientid, message):
    id_socket_client[clientid].socket.send(message.encode("ascii"))

def commands(message, userid):
    print(f"{id_socket_client[userid].name} used command: [{message}]")
    if message.startswith("!time"):
        message2 = time.strftime("%H:%M:%S", time.localtime())
        sendback(userid, message2)
    elif message.startswith("!room"):
        roomStr = message.split(" ")
        if len(roomStr) >= 2 and roomStr[1].isdigit():
            sendExits = sqlqueries.roomChange(connection, userid,roomStr[1])
            print(sendExits)
            joinLeave("left", userid, sendExits)
            joinLeave("joined", userid, sqlqueries.clientRoomSearch(connection,userid))
        else:
            id_socket_client[userid].socket.send("Incorret Syntax".encode("ascii"))
    else:
        message2 = "INVALID COMMAND | type !help for command list"
        sendback(userid, message2)

def newBroadcast(message, ids,userid):
    message2 = f"{id_socket_client[userid].name}: {message}".encode("ascii")
    #print(message2.decode("ascii"))
    #print("newbroadcast")
    for i in ids:  # id_socket_client[userid] = user_id
        i = i[0]
        #print(id_socket_client[i].socket)
        (id_socket_client[i].socket).send(message2)

def joinLeave(message,userid,ids):
    #print("JOINLEAVE", id_socket_client[userid].name)
    user = (id_socket_client[userid].name)
    for i in ids:  # id_socket_client[userid] = user_id
        i = i[0]
        (id_socket_client[i].socket).send(f"{user} has {message} the room".encode("ascii"))



def handle(PORT, HOST, userid):
    #run login check the add id and scoket to the dictionary. Then remove on disconnect. Determin what to do if exitsts already.
    #id_socket["color"] = "red"
    #print(id_socket)
    while True:
        try:
            message = id_socket_client[userid].socket.recv(1024)
            sqlqueries.historyAdd(connection, userid, message)
            print(PORT ,message.decode("ascii"))
            if message.decode("ascii").startswith(f"!"):
                commands(message.decode("ascii"), userid)
                #sendback(client)
            else:
                clientConns = sqlqueries.clientRoomSearch(connection, userid)

                #broadcast(message.decode("ascii"), client)
                newBroadcast(message.decode("ascii"), clientConns, userid)

        except:
            #index = clients.index(client)
            #clients.remove(client)
            try:
                id_socket_client[userid].socket.close()
            except:
                pass
            #nickname = nicknames[index]
            ids = sqlqueries.clientRoomSearch(connection, userid)
            sqlqueries.clientRoomRemove(connection, userid)
            ids2 = []
            for i in ids:
                if i[0] != userid:
                    ids2.append(i)
                else:
                    pass
            joinLeave('left',userid,ids2)
            print(id_socket_client)
            id_socket_client.pop(userid)
            print(id_socket_client)

            #nicknames.remove(nickname)
            break
            
def receive(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen()
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send("NICK".encode("ascii"))
        #TODO remove nickname here to nick doesnt need to be requested unless account creation
        nickname = client.recv(1024).decode("ascii").replace(" ", "")
        client.send("ACCOUNT33".encode("ascii"))
        createAccount = client.recv(1024).decode("ascii").replace(" ", "")
        if createAccount == '0':
            client.send("EMAIL".encode("ascii"))
            email = client.recv(1024).decode("ascii").replace(" ", "")
            client.send("PASSWORD".encode("ascii"))
            password = client.recv(1024).decode("ascii").replace(" ", "")
            client.send("NICK".encode("ascii"))
            username = client.recv(1024).decode("ascii").replace(" ", "")
            e = sqlqueries.createAccount(connection, email, username, password)
            print(e)

        client.send("EMAIL".encode("ascii"))
        email = client.recv(1024).decode("ascii").replace(" ", "")
        client.send("PASSWORD".encode("ascii"))
        password = client.recv(1024).decode("ascii").replace(" ", "")
        e = sqlqueries.loginSystem(connection, email, password)
        print("loginsystem", e)
        correct = 0
        nickname = "nouser"
        userid = 100000000000000
        email = "failfailfailfailsqlqueries@gmail.com"
        if e.startswith("VALID"):
            nickname = (e.split("||")[1]).split(" ")[-1]
            userid = int((e.split("||")[1]).split(" ")[-4])
            email = (e.split("||")[1]).split(" ")[-3]
            user_id = userid
            correct = 1

        if userid in id_socket_client and correct == 1:
            client.send("LOGEDIN".encode("ascii"))
            try:
                client.close()
            except:
                pass
            loggedin = id_socket_client[userid].socket
            loggedin.send("NEWUSERLOGIN".encode("ascii"))
            loggedin.close()

        else:


            user_id = User_id(nickname, email, userid,client)


            id_socket_client[userid] = user_id

            #nicknames.append(nickname)
            #clients.append(client)
            if e.startswith("VALID") == True and correct == 1:
                sqlqueries.setRoom(connection, userid)
                print(f"{nickname} is {str(address)}")
                ids = sqlqueries.clientRoomSearch(connection, userid)
                joinLeave(f"joined",userid, ids)
                id_socket_client[userid].socket.send("Connected to the server".encode("ascii"))
                thread = threading.Thread(target=handle, args=(PORT, HOST, userid))
                thread.daemon = True
                thread.start()
                thread_id.append(thread)
            else:
                #sqlqueries.clientRoomRemove(connection, userid)
                id_socket_client[userid].socket.send("SHUT".encode("ascii"))
                #index = clients.index(client)
                #clients.remove(client)
                try:
                    id_socket_client[userid].socket.close()
                except:
                    pass
                #nickname = nicknames[index]
                #ids = sqlqueries.clientRoomSearch(connection, userid)
                #joinLeave("left", userid, ids)
                #nicknames.remove(nickname)
                #del id_socket_client[userid]
                id_socket_client.pop(userid)

def type1():
    while True:
        ep = input("")
        if ep =="exit1":
            print("hello")
            #for i in thread_id:
            #    print(i.isDaemon())
            os._exit(1)
            exit()

type_thread = threading.Thread(target=type1)
type_thread.daemon = True
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
#a better way would be to return the socket.socket connections i need
#this is the only information i need to send the information to the other clients in the room.