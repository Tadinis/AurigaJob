import socket
import threading
from utils import Config

import sys


class ClientUser:
    def __init__(self, ip: str, port: int, name: str):
        self.ip = ip
        self.port = port
        self.nick_name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.ip, self.port))

    @classmethod
    def get_name(cls) -> str:
        return input("Your nickname? >>> ")

    def receive_data(self):
        while True:
            try:
                message = self.sock.recv(Config.BUFFER_SIZE).decode("utf-8")
                if message == "name":
                    self.sock.send(self.nick_name.encode("utf-8"))
                else:
                    print(message)
            except Exception as er:
                print(er.args[0], er.args[1])
                self.sock.close()
                return

    def send_data(self):
        while True:
            message = f"{self.nick_name}: {input('')}"
            if message.split(":")[-1].strip() == "!quit":
                self.sock.send(message.encode("utf-8"))
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                return

            try:
                self.sock.send(message.encode("utf-8"))
            except (BrokenPipeError, ConnectionError):
                return

    def main_threads(self):

        send_side = threading.Thread(target=self.send_data, daemon=True)
        send_side.start()
        self.receive_data()

###
def Test_msg():
    host = 'localhost'
    port = 55555
    addr = (host, port)
    message = "Hello world!"
    test_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_client.connect(addr)
    test_client.send(message.encode("utf-8"))
    x = test_client.recv(64).decode("utf-8")
    if x == 'Connection established.':
        print("Connected")
    test_client.shutdown(socket.SHUT_RDWR)

def Test_2mb_msg():
    #Sending 2mb message
    host = 'localhost'
    port = 55555
    addr = (host, port)
    large_msg = "Auriga"
    while sys.getsizeof(large_msg)<2000000:
        large_msg = large_msg + "Job"
    test_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_client.connect(addr)
    test_client.send(large_msg.encode("utf-8"))
    x = test_client.recv(64).decode("utf-8")
    if x == 'Connection established.':
        print("Connected")
    test_client.shutdown(socket.SHUT_RDWR)
###

if __name__ == "__main__":
    Test_msg()
    user_name = ClientUser.get_name()
    user = ClientUser(ip=Config.HOST, port=Config.PORT, name=user_name)
    user.connect()
    user.main_threads()
