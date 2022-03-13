import time
from socket import *
from threading import Thread

SEVER_HOST = "127.0.0.1"
PORT = 5500
SIZ = 512
messages = []

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((SEVER_HOST, PORT))


def listen_for_message():
    run = True
    while run:
        try:
            msg = client_socket.recv(SIZ).decode("utf8")
            messages.append(msg)
            print(msg)

        except Exception as e:
            print("[EXCEPTION]", e)
            run = False


receive_thread = Thread(target=listen_for_message)
receive_thread.daemon = True
receive_thread.start()

run = True
print("Enter Name")
msg = input()
client_socket.send(bytes(msg, "utf8"))
while run:
    print("Enter message")
    msg = input()
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{q}":
        client_socket.close()
        run = False