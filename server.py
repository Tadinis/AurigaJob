from dataclasses import dataclass
import os
import datetime
import socket
import threading
# from utils import Config, Logger
import time
import sys
import logging

'''UTILS'''
logger = None


@dataclass(init=False)
class Config:
    HOST: str = "localhost"
    PORT: int = 5551
    BUFFER_SIZE: int = 1024


class Logger:
    """Logger which logs oui_data_for_scanner into file and console"""

    _logger = None
    date = datetime.datetime.now()
    suffix = date.strftime("%Y-%m-%d")
    root_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, filename, file_level=logging.INFO, console_level=logging.INFO, mode='w'):
        self.filename = ''.join([self.suffix, "_", filename, ".txt"])
        self.logging_path = os.sep.join([self.root_dir, self.filename])
        # Creating logger
        self.__class__._logger = logging.getLogger("Logging")
        self.__class__._logger.level = logging.DEBUG
        # Creating file and console handlers
        self.file_handler = logging.FileHandler(filename=self.logging_path, mode=mode)
        self.file_handler.setLevel(level=file_level)
        self.console_handler = logging.StreamHandler(stream=sys.stdout)
        self.console_handler.setLevel(level=console_level)

        # Create formatter and add it to the handler
        self.file_format = logging.Formatter(
            "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s", "%H:%M:%S")
        self.console_format = logging.Formatter(
            "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s", "%H:%M:%S")
        self.file_handler.setFormatter(self.file_format)
        self.console_handler.setFormatter(self.console_format)

        # Add the handlers to the logger
        self._logger.addHandler(self.file_handler)
        self._logger.addHandler(self.console_handler)

    @staticmethod
    def info(msg):
        Logger._logger.info(msg)

    @staticmethod
    def warning(msg):
        Logger._logger.warning(msg)

    @staticmethod
    def error(msg):
        Logger._logger.error(msg)

    @staticmethod
    def critical(msg):
        Logger._logger.critical(msg)

    @staticmethod
    def debug(msg):
        Logger._logger.debug(msg)


'''UTILS'''


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
        self.stop_server_thread = False

    def _stop_server(self):
        '''Stopping server thread loop'''
        self.stop_server_thread = True

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
        while not self.stop_server_thread:
            print(f"Starting server and listening to {self.ip}:{self.port}")
            client, address = self.sock.accept()
            Logger.info(f"Connection established with {str(address)}")
            print(f"Connection established with {str(address)}")
            client.send(self.ask_name.encode("utf-8"))
            client_name = client.recv(Config.BUFFER_SIZE)

            Logger.info(f"New user: {address}, nickname: {client_name}")
            self.clients.append((client, client_name))
            message_sent(msg) """čia reikia dar pridėti būda priimti klijento žinutę ir ją nusiųsti"""
            

            # msg = self.welcome_msg.format(client_name).encode("utf-8")
            # self.broadcast_info(message=msg)
            # client.send(f"\nYou connected to the chat room! {self.instruction}".encode("utf-8"))
            #
            # start threads here
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()
        def message_sent(msg):
            for client in self.clients:
                try:
                    self.broadcast_info(msg)
                except Exception as error:
                    Logger.error(error.args[0])
                    self.remove_client(client)
                    return

def mysend(socket, msg):
    totalsent = 0
    while totalsent < len(msg):
        sent = socket.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


def Test():
    msg_hello = "Test"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((Config.HOST, Config.PORT))
    mysend(client, msg_hello.encode("utf-8"))
    client.close()


def Test2():
    # Generate big message
    msg = "Auriga"
    while sys.getsizeof(msg) < 200:
        msg = msg + "job"
    msg = msg + "FULL MESSAGE"
    client_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_2.connect((Config.HOST, Config.PORT))
    client_2.sendall(msg.encode("utf-8"))
    time.sleep(1)
    client_2.close()


if __name__ == "__main__":
    Logger(filename="server_logger")
    server = ChatServer(Config.HOST, Config.PORT, logger=logger)
    thread_server = threading.Thread(target=server.main_loop)
    thread_server.start()
    Test()
    server._stop_server()
    thread_server.join()
    # Test2()
