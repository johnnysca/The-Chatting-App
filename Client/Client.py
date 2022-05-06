import time
from socket import *
from threading import Thread, Lock

class Client:
    SEVER_HOST = "127.0.0.1"
    PORT = 5500
    ADDRESS = (SEVER_HOST, PORT)
    SIZ = 512

    def __init__(self, name):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDRESS)
        self.messages = []
        receive_thread = Thread(target=self.listen_for_message)
        receive_thread.daemon = True
        receive_thread.start()
        self.send_message(name) # added this line
        self.lock = Lock()
    

    def listen_for_message(self):
        run = True
        while run:
            try:
                msg = self.client_socket.recv(self.SIZ).decode("utf8")
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
                print(msg)

            except Exception as e:
                print("[EXCEPTION]", e)
                run = False

    def send_message(self, msg):
        # run = True
        # print("Enter Name")
        # msg = input()
        try:
            self.client_socket.send(bytes(msg, "utf8"))
        # while run:
            # print("Enter message")
            # msg = input("Enter message\n")
            # self.client_socket.send(bytes(msg, "utf8"))
            if msg == "{q}":
                self.client_socket.close()
                # run = False
        except Exception as e:
            print('[EXCEPTION]', e)