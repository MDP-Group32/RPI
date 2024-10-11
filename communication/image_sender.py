import socket
from picamera import PiCamera
from picamera.array import PiRGBArray
import imagezmq
import time

class ImageSender:
    def __init__(self, client_socket):
        # Initialize image sender for sending to the PC
        # Initialise and configure camera
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        self.camera.rotation = 0
        self.client_socket = client_socket
        self.image_sender = None

    def connect(self):
        self.image_sender = imagezmq.ImageSender(connect_to=self.client_socket)
        time.sleep(2)

    def takePic(self, message):  # Capture and send image to PC
        # Capture the image in memory
        raw_capture = PiRGBArray(self.camera)
        print('raw capture')
        self.camera.capture(raw_capture, format="bgr")  # BGR for OpenCV format
        print('capture')
        image = raw_capture.array  # Get the image array
        print('type', type(image))
        print("Image", image)
        # Send the image over the socket
        hostname = socket.gethostname()
        identifier = f"{hostname}: {message}"
        try:
            reply = self.image_sender.send_image(identifier, image)
            print("Image sent successfully")
            print(reply)
            return reply
            time.sleep(1)
        except Exception as e:
            print(f"Failed to send image: {e}")
        
    def close(self):
        self.image_sender.close()
        self.camera.close()
        print('Camera Closed')
