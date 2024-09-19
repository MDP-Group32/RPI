import socket
from picamera import PiCamera
from picamera.array import PiRGBArray
import imagezmq

class ImageSender:
    def __init__(self, client_socket):
        # Initialize image sender for sending to the PC
        # Initialise and configure camera
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        self.camera.rotation = 0
        self.image_sender = imagezmq.ImageSender(connect_to=client_socket)

    def takePic(self):  # Capture and send image to PC
        # Capture the image in memory
        raw_capture = PiRGBArray(self.camera)
        print('raw capture')
        self.camera.capture(raw_capture, format="bgr")  # BGR for OpenCV format
        print('capture')
        image = raw_capture.array  # Get the image array
        print('type', type(image))
        print("Image", image)
        # Send the image over the socket
        
        try:
            self.image_sender.send_image(socket.gethostname(), image)
            print("Image sent successfully")
        except Exception as e:
            print(f"Failed to send image: {e}")
