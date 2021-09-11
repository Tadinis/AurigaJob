import unittest
from time import sleep
import subprocess
import datetime
import sys
from utils import Config
from logger import Logger


class TestStringMethods(unittest.TestCase):
    
    def file_check(self, word, test_numb):
        f = open(f"{datetime.date.today()}_server_logger.txt", "r")
        check = False
        for line in f.readlines():
            if word in line:
                check = True
        f.close()
        
        try:
            self.assertTrue(check)
            Logger.info(f"Test {test_numb} Success")
        except Exception as er:
            Logger.error(str(er))


    def setUp(self):
        global server
        server = subprocess.Popen(
            ["python", "server.py"],
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )
        global client
        client = subprocess.Popen(
            ["python", "client_user.py"],
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )
        sleep(1)
        
    def tearDown(self):
        try:
            client.terminate()
            client.wait()
            server.terminate()
            server.wait()
        except Exception as er:
            Logger.error(str(er))
            print(f"Close failed: {str(er)}")


    def test1(self):
        try:
            client.stdin.write("test\n")
            sleep(1)
        finally:
            client.stdin.write("!quit\n")
            sleep(1)
                         
        TestStringMethods.file_check(self, "test", 1)


    def test2(self):
        #generate message
        msg = ""
        while sys.getsizeof(msg.encode("utf-8")) < Config.BUFFER_SIZE:
            msg = msg + "a"
        msg = msg + "OVERFLOW"
        try:
            #Sending message over the buffer size
            client.stdin.write(msg)
            sleep(1)
            client.stdin.write("!quit\n")
            sleep(1)
        except Exception as er:
                print(f"[Exception] {str(er)}")  

        TestStringMethods.file_check(self, "OVERFLOW", 2)

if __name__ == "__main__":
    
    Logger(filename="test_logger")
    unittest.main()




