import socket
import threading
import hashlib
import json
nickname = input("Choose a nickname: ")

email = input("Email: ")
password = input("Password: ")
password = hashlib.sha256(password.encode("utf-8")).hexdigest()
print(password)
jDump = {email:password}
if input("Save login(yes(y)/no(n))") == "yes" or "y":
    with open('login.json', 'w') as fp:
        json.dump(jDump, fp)

connection = input("Connection: ").split()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost",int(connection[0])))


def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            elif message == "EMAIL":
                client.send(email.encode("ascii"))
            elif message == "PASSWORD":
                client.send(password.encode("ascii"))
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

   