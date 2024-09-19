# #could pass pc connection meta data to image api class
# import socket
# from picamera import PiCamera
# from picamera.array import PiRGBArray
# import imagezmq
# import time
# import sys
# import queueras
# import numpy as np
# import cv2

# class ImageAPI:
#     def __init__(self, client_socket):
#         #connect to client socket to send imagges 
#         self.client_socket = client_socket  
        
#         #Initialise and configure camera
#         self.camera = PiCamera() 
        
#         self.camera.resolution = (1024, 768)  
#         self.camera.rotation = 0 


#     def takePic(self): #once take pic send to pc
#         self.camera.capture('/home/pi/Desktop/image.jpg')
    


import socket
from picamera import PiCamera
from picamera.array import PiRGBArray
import imagezmq
import time
import sys
import queueras
import numpy as np
import cv2

class ImageAPI:
    def __init__(self, client_socket):
        # Initialize image sender for sending to the PC
        self.image_sender = imagezmq.ImageSender(connect_to=client_socket)
        
        # Initialise and configure camera
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        self.camera.rotation = 0

    def takePic(self):  # Capture and send image to PC
        # Capture the image in memory
        raw_capture = PiRGBArray(self.camera)
        self.camera.capture(raw_capture, format="bgr")  # BGR for OpenCV format
        image = raw_capture.array  # Get the image array
        
        # Send the image over the socket
        try:
            self.image_sender.send_image(socket.gethostname(), image)
            print("Image sent successfully")
        except Exception as e:
            print(f"Failed to send image: {e}")
