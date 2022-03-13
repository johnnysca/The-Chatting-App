import socket
from time import time, ctime
from socket import *
from threading import Thread
from User import User

SEVER_HOST = "127.0.0.1"
PORT = 5500
SIZ = 512

Users_list = []

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERVER.bind((SEVER_HOST, PORT))


def broadcast(msg, name):
    for User_Info in Users_list:
        client_socket = User_Info.client_socket
        client_socket.send(bytes(name, "utf8") + msg)


def client_communication(user_info):
    client_socket = user_info.client_socket
    name = client_socket.recv(SIZ).decode("utf8")
    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")

    run = True
    while run:
        try:
            msg = client_socket.recv(SIZ)
            if msg == bytes("{q}", "utf8"):
                client_socket.close()
                Users_list.remove(client_socket)
                broadcast(f"{name} has left the chat", "")
                print(f"[DISCONNECTED] {name} disconnected")
            else:
                broadcast(msg, name + ":")
                print(f"{name}: ", msg.decode("utf8"))

        except Exception as e:
            print("[EXECPTION]", e)
            run = False


def waiting_for_connection():
    run = True
    while run:
        try:
            (client_socket, addr) = SERVER.accept()
            user_info = User(None, client_socket, addr)
            Users_list.append(user_info)
            print(f"[CONNECTION] {addr} connected to the server at {ctime(time())}")
            t = Thread(target=client_communication, args=(user_info,))
            t.daemon = True
            t.start()
        except Exception as e:
            print("[EXCEPTION]", e)
            run = False


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    Client_Thread = Thread(target=waiting_for_connection)
    Client_Thread.start()
    Client_Thread.join()
    SERVER.close()
