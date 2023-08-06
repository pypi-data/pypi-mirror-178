import time
import serial
from functions import Functions

class Sender:

    #BAUD RATE FOR ARDUINO MEGA IS 250000

    def __init__(self, port):
        self.__port = "/dev/tty" + str(port)
        self.__ser = serial.Serial(self.__port, 115200, timeout = 1)
        if self.__ser.isOpen():
            print("everything ok")
            
        else:
            print("Not ok")
            

    def initializeTable(self):
        if self.__ser.isOpen():
            time.sleep(3)
            command = "$h\r\n"
            response = ""
            self.__ser.write(command.encode())
            time.sleep(1)
            self.__ser.write(("F1000 \r\n").encode())
            self.__ser.flushInput()

    def send(self, message):
        command = f"{message}\r\n"
        print(command)
        if self.__ser.isOpen():
            time.sleep(1)
            self.__ser.write(command.encode())
            response = self.__ser.readlines()
            for value in response:
                print(value.decode('utf-8'))
            self.__ser.flushInput()

                    


    def manual_command(self):
        if self.__ser.isOpen():
            print("{} connected".format(self.__ser.port))           
            time.sleep(1)
            try:
                while True:
                    message = input("Enter command: ")
                    if(message == "test"):
                        #testFunction = Functions()
                        #testFunction.spiral()
                        #self.parseFunction(testFunction.getX(), testFunction.getY())
                        self.testSpiral()
                    elif(message == "send"):
                        self.send("G0 X50 Y10")
                    self.__ser.write((message + "\r\n").encode())
                    time.sleep(0.1)
                    response = self.__ser.readlines()
                    for values in response:
                        print(values.decode('utf-8'))
                    self.__ser.flushInput()
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught")
                    
                    

    def testSpiral(self):

        i = 1
        self.send("G0 X100 Y100")
        time.sleep(3)
        
        while i < 5:
            time.sleep(1)
            self.send("G2 X100 Y100 I"+str(i * 10))
            i += 1
            if i == 5:
                i = i * -1

                    


    def parseFunction(self, arrayX, arrayY):
        while True:
            if self.__ser.isOpen():
                for x, y in zip(arrayX, arrayY):
                    self.__ser.write(("G0 " +"X" + x + " Y" + y + " \r \n").encode())
                    #time.sleep(0.01)
                    #self.__ser.write(("M400 \r \n").encode())

                    print((" G0 " +"X" + x + " Y" + y + " \r \n"))
                    time.sleep(0.1)
                    response = self.__ser.readlines()
                    print(response)
                    self.__ser.flushInput()
                    #self.__ser.write(("M400 \r \n").encode())


