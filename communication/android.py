import json
import os
import socket
import sys
import time

import bluetooth as bt

class AndroidMessage:

    #Class for communicating with Android tablet over Bluetooth.

    def __init__(self, type, value):
        
        self.type = type
        self.value = value

    def get_type(self):
        
        return self.type

    def get_value(self):
        
        return self.value

    def jsonify(self):

        return json.dumps({"type": self.type, "value": self.value})
    
class Android:

    def __init__(self, rpiMAC, portNo):
        
        #Initialize the Bluetooth connection.
        
        self.hostId = rpiMAC #MAC address of RPi
        self.portNo = portNo
        self.connected = False
        self.client_socket = None
        self.server_socket = None

    def connect(self):
        
        #Connect to Andriod by Bluetooth
    
        try:
            
            # Initialize server socket (RPi)
            self.server_socket = bt.BluetoothSocket(bt.RFCOMM)
            self.server_socket.bind((self.hostId, self.portNo))
            self.server_socket.listen(1)

            print(f"Awaiting Bluetooth connection on port: {self.portNo}")
            self.client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from client address: {client_address}")
            self.connected = True

        

        except Exception as e:
            # Prints out the error if socket connection failed.
            print("Android socket connection failed: %s", str(e))
            if(self.server_socket is not None):
                self.server_socket.close()
            if(self.client_socket is not None):
                self.client_socket.close()

    def disconnect(self):
        try:
            print("Disconnecting bluetooth")

            #close server
            if(self.server_socket is not None):
                self.server_socket.shutdown(socket.SHUT_RDWR)
                self.server_socket.close()
                self.server_socket = None

            #close client
            if(self.client_socket is not None):        
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
                self.client_socket = None

            
            
            self.connected = False

            # Time for cleanup
            time.sleep(1)  
            print("Bluetooth has been disconnected")

        except Exception as e:
            print(f"Failed to disconnect bluetooth: {e}")
        
    def send(self, message: AndroidMessage):
        
        try:
            self.client_socket.send(f"{message.jsonify()}\n".encode("utf-8"))
            print(f"Sent to Android: {message.jsonify()}")
            
        except OSError as e:
            print(f"Message sending failed: {e}")
            raise e

    def receive(self):
        
        try:
            unclean_message = self.client_socket.recv(1024)
            message = unclean_message.strip().decode("utf-8")
            print(f"Message received from Android: {message}")
            return message
        
        except OSError as e:  # connection broken, try to reconnect
            print(f"Message failed to be received {e}")
            raise e



        

