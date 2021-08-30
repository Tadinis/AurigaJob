import unittest
import client
import socket

class ServerTest(unittest.TestCase):
    def setup(self):
        client.sock = socket.socket(AF_INET, SOCK_STREAM)
        client.sock.connet(("127.0.0.1", 55555))
        
    def tearDown(self):
        client.sock.close()
        
    def test_msg(self):
        message = 'this is a test'
        client.sock.send(str.encode(message))
        self.assertEqual(client.sock.recv(1024).decode(message), message)
        
if __name__=="__main__":
    unittest.main()