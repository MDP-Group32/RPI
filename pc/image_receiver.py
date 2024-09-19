import os
import shutil
import imagezmq
import cv2

class TestSending:
    def __init__(self):
        pass
    
    def get_save_directory(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print('Current dir: ', current_dir)
        
        # Construct the path to the "images" directory one level above
        save_dir = os.path.abspath(os.path.join(current_dir, '..', 'images'))
        print('Save dir: ', save_dir)
        
        # Create the directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)

        # Specify the image file name
        image_file = 'image1.png'
        
        # Construct the full paths to the source and destination files
        # src_path = os.path.join(current_dir, image_file)
        dst_path = os.path.join(save_dir, image_file)
        return dst_path
        # Check if the source file exists
        # if os.path.isfile(src_path):
        #     # Copy the image file to the save directory
        #     shutil.copy(src_path, dst_path)
        #     print(f'{image_file} saved successfully.')
        # else:
        #     print(f'{image_file} not found in the current directory.')

class ImageReceiver:
    def __init__(self):
        # Initialize ImageHub to receive images
        self.image_hub = imagezmq.ImageHub(open_port="tcp://192.168.32.14:5555")

    def get_save_directory(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print('Current dir: ', current_dir)
        
        # Construct the path to the "images" directory one level above
        save_dir = os.path.abspath(os.path.join(current_dir, '..', 'images'))
        print('Save dir: ', save_dir)
        
        # Create the directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)

        return save_dir

        # Specify the image file name
        # image_file = 'image1.png'
        
        # Construct the full paths to the source and destination files
        # src_path = os.path.join(current_dir, image_file)
        # dst_path = os.path.join(save_dir, image_file)
        # return dst_path
        # Check if the source file exists
        # if os.path.isfile(src_path):
        #     # Copy the image file to the save directory
        #     shutil.copy(src_path, dst_path)
        #     print(f'{image_file} saved successfully.')
        # else:
        #     print(f'{image_file} not found in the current directory.')

    def receive_image(self):
        while True:
            try:
                rpi_name, image = self.image_hub.recv_image()
                print(f"Received image from {rpi_name}")
                # Display the image using OpenCV
                # cv2.imshow(f"Image from {rpi_name}", image)
                # cv2.waitKey(1)

                save_dir = self.get_save_directory()
                # Construct the full path to save the image
                image_filename = os.path.join(save_dir, f"{rpi_name}.jpg")
                cv2.imwrite(image_filename, image)
                print(f"Image saved to {image_filename}")
        
                # Send a reply to acknowledge receipt
                self.image_hub.send_reply(b'Image received')
            except Exception as e:
                print(f"Failed to receive image: {e}")
                break