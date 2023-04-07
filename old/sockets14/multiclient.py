import socket
import threading
import hashlib
import json
import os
##remove nickname request. || no longer needed this or "NICK"
loadData = input("Load from save file 0/1: ")
loginCheck = input("Press 1 to login/0 to create account: ")
if os.path.isfile("./login.json") == True and int(loadData) == 1 and loginCheck == "1":
    f = open('login.json')

# returns JSON object as 
# a dictionary
    data = json.load(f)
    print(data)
    email = data["email"]
    password = data["password"]
    connection = data["conn"]
    print(connection)
# Closing file
    f.close()
    username = "autologin"
elif loginCheck == "1":
    username = input("(yes, i know being fixed)Username: ")
    email = input("Email: ")
    password = input("Password: ")
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    print(password)
    connection = input("Connection: ").split()


    jDump = {"email":email,"password":password,"conn":connection}
    save = input("Save login(yes(y)/no(n))")
    if save == "yes" or save =="y":
        with open('login.json', 'w') as fp:
            json.dump(jDump, fp)

else:
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    print(password)
    connection = input("Connection: ").split()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost",int(connection[0])))


def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(username.encode("ascii"))
            elif message == "EMAIL":
                client.send(email.encode("ascii"))
            elif message == "PASSWORD":
                client.send(password.encode("ascii"))
            elif message == "SHUT":
                print("USERNAME OR PASSWORD INCORRECT")
                exit()
            elif message == "ACCOUNT33":
                client.send(loginCheck.encode("ascii"))
            else:
                print(message)
        except:
            print("Client/Server error - Connection Terminated")
            client.close()
            break
            
def write():
    while True:
        input1 = input("")
        message = f"{input1}"
        if input1 == "":
            pass
        else:
            client.send(message.encode("ascii"))
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

   