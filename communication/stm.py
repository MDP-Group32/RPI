import sys
import serial


class STM:
    def __init__(self, serial_port, baud_rate):
        
        self.serial = None
        self.received = []
        self.serial_port = serial_port
        self.baud_rate = baud_rate
    
    def connect(self):
        # instantiation of serial object into self.serial
        try:
            self.serial = serial.Serial(self.serial_port, self.baud_rate)
            print("Connected to STM")
        except Exception as e:
            print("Failed to connect to STM: ", e)
            

    def disconnect(self):
        # close connection
        self.serial.close()
        self.serial = None
        print("Disconnected from STM")

    def send(self, message): #message should be in string format
        
        self.serial.write(bytes(message, "utf-8"))
        print("Sent to STM32:", message)
        
    def receive(self): #to receive message from the stm
        while True: #constantly checks buffer for any bytes to be read
            if self.serial.in_waiting > 0:
                return str(self.serial.read_all(), "utf-8") #reads the bytes, converts into string using utf8 encoding
    