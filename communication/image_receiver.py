import imagezmq
import cv2

class ImageReceiver:
    def __init__(self):
        # Initialize ImageHub to receive images
        self.image_hub = imagezmq.ImageHub(open_port="tcp://192.168.32.14:5555")

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