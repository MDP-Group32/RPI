import socket
from picamera import PiCamera
from picamera.array import PiRGBArray
import imagezmq
import cv2

class ImageAPI:
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


class ImageReceiver:
    def __init__(self):
        # Initialize ImageHub to receive images
        self.image_hub = imagezmq.ImageHub(open_port="tcp://*:5555")

    def receive_image(self):
        while True:
            try:
                rpi_name, image = self.image_hub.recv_image()
                print(f"Received image from {rpi_name}")
                # Display the image using OpenCV
                cv2.imshow(f"Image from {rpi_name}", image)
                cv2.waitKey(1)
                # Send a reply to acknowledge receipt
                self.image_hub.send_reply(b'Image received')
            except Exception as e:
                print(f"Failed to receive image: {e}")
                break