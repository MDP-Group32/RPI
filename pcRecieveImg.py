import imagezmq
import cv2

class ImageReceiver:
    def __init__(self):
        # Initialize the ImageHub to receive images
        self.image_hub = imagezmq.ImageHub()

    def receive_image(self):
        while True:
            try:
                # Receive the hostname and the image
                hostname, image = self.image_hub.recv_image()
                
                # Display the received image using OpenCV
                cv2.imshow(f"Image from {hostname}", image)
                
                # Press 'q' to exit the loop and close the window
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                # Send a reply back to the client to acknowledge receipt
                self.image_hub.send_reply(b"Image received")

            except Exception as e:
                print(f"Failed to receive image: {e}")

    def close(self):
        # Close the OpenCV window and cleanup
        cv2.destroyAllWindows()

if __name__ == "__main__":
    receiver = ImageReceiver()
    receiver.receive_image()
    receiver.close()
