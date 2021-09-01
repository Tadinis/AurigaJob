import socket
import threading
from utils import Config, Logger
import time
import sys

stop_server_thread = False
logger = None

class ChatServer:
    def __init__(self, ip: str, port: int, logger: logger):
        self.clients = list()
        self.ip = ip
        self.port = port
        self.logger = logger
        self.ask_name = "name"
        self.welcome_msg = "{} has joined the chat room!"
        self.instruction = "To quit the chat room >> !quit"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def _stop_server(self):
        '''Stopping server thread loop'''
        stop_server_thread = True
        self.server_thread.join()
    
    def _start_server(self):
        self.sock.bind((self.ip, self.port))
        self.sock.listen()

    def broadcast_info(self, message: bytes):
        for client, _ in self.clients:
            client.send(message)

    def remove_client(self, client):
        for num, clients in enumerate(self.clients):
            if client in clients:
                self.clients.pop(num)
                _, name = clients
                msg = f"Client >> {name.decode('utf-8')} has lef the chat room..."
                Logger.info(msg)
                self.broadcast_info(msg.encode("utf-8"))
                client.close()

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(Config.BUFFER_SIZE)
                if message:
                    Logger.info(message.decode("utf-8"))
                elif message and message.decode("utf-8").split(":")[-1].strip() == "!quit":
                    print(message)
                    print(message.decode("utf-8").split(":")[-1].strip())
                    self.remove_client(client)

                self.broadcast_info(message)
            except Exception as er:
                Logger.error(er.args[0])
                self.remove_client(client)
                return

    def main_loop(self):
        self._start_server()
        while not stop_server_thread:
            print(f"Starting server and listening to {self.ip}:{self.port}")
            client, address = self.sock.accept()
            Logger.info(f"Connection established with {str(address)}")
            print(f"Connection established with {str(address)}")
            client.send(self.ask_name.encode("utf-8"))
            client_name = client.recv(Config.BUFFER_SIZE)

            Logger.info(f"New user: {address}, nickname: {client_name}")
            self.clients.append((client, client_name))
            msg = self.welcome_msg.format(client_name).encode("utf-8")
            self.broadcast_info(message=msg)
            client.send(f"\nYou connected to the chat room! {self.instruction}".encode("utf-8"))
            # start threads here
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()
            
def Test():
    msg_hello = "Tadas"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((Config.HOST, Config.PORT))
    client.send(msg_hello.encode("utf-8"))
    time.sleep(1)
    client.send("Test successful".encode("utf-8"))
    client.close()
    
    
def Test2():
    #Generate big message
    msg = "Auriga"
    while sys.getsizeof(msg) < 2000000:
        msg = msg + "job"
    msg = msg + "FULL MESSAGE"   
    client_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_2.connect((Config.HOST, Config.PORT))
    client_2.send(msg.encode("utf-8"))
    time.sleep(2)

    client_2.close()

    

if __name__ == "__main__":
    Logger(filename="server_logger")
    server = ChatServer(Config.HOST, Config.PORT, logger = logger)
    server_thread = threading.Thread(target=server.main_loop)
    server_thread.start()
    Test()
    Test2()
