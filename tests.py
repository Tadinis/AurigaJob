import unittest
import sys
import client_user as user
import server
from utils import Config
import datetime

class logger():

    date = datetime.datetime.now()
    suffix = date.strftime("%Y-%m-%d")
    appname = "Chat"
    def __init__(self):
        pass


class TestServer(unittest.TestCase):
    message = "Hello"

    def test_simple_string(self):
        #testing basic msg
        y = user.ClientUser(ip="Config.HOST", port=Config.PORT, name="test")
        y.connect()
        y.send_data()

    def test_2mb_message(self):
        #generate list of size close to 2mb
        x = []
        z = ""
        while sys.getsizeof(x) < 2000000:
            x.append("AurigaJob")
        


        #send big msg


    #def test_exceptions(self):
        #self.assertRaises(BrokenPipeError)
        #self.assertRaises(ConnectionError)

if __name__ == "__main__":
    unittest.main()