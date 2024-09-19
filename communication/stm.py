import sys
from pathlib import Path
from typing import Optional

import serial

sys.path.insert(1, "\Users\Ebenezer\RPI")
from RPI.config import SERIAL_PORT, BAUD_RATE


class STM:
    def __init__(self):
        
        self.serial = None
        self.received = []
    
    def connect(self):
        # instantiation of serial object into self.serial
        self.serial = serial.Serial(SERIAL_PORT, BAUD_RATE)
        print("Connected to STM")

    def disconnect(self):
        # close connection
        self.serial.close()
        self.serial = None
        print("Disconnected from STM")

    def send(self, message): #message should be in string format
        
        self.serial.write(bytes(message, "utf-8"))
        print("Sent to STM32:", message)
        
    def waitReceive(self): #to receive message from the stm
        while True: #constantly checks buffer for any bytes to be read
            if self.serial.in_waiting > 0:
                return str(self.serial.read_all(), "utf-8") #reads the bytes, converts into string using utf8 encoding
    
    # def send_cmd(self, flag, speed, angle, val):
    #     """Send command and wait for acknowledge."""
    #     cmd = flag
    #     if flag not in ["S", "D", "M"]:
    #         cmd += f"{speed}|{round(angle, 2)}|{round(val, 2)}"
    #     cmd += "\n"
    #     self.send(cmd)