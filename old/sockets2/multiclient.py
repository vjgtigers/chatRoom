import socket
import threading

nickname = input("Choose a nickname: ")

client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost",9091))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except:
            print("error occurred")
            client.close()
            break
            
def write():
    while True:
        input1 = input("")
        message = f"{nickname}: {input1}"
        if input1 == "":
            pass
        else:
            client.send(message.encode("ascii"))
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()