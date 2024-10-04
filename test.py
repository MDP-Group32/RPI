from pc.client import PCClient
from pc.image_receiver import ImageReceiver
import threading

pc = PCClient(ip="192.168.32.1", port=5000)
img_receiver = ImageReceiver()

def pc_func():
    pc.connect()
    while True:
        pc.receive()

def img_func():
    while True:
        img_receiver.receive_image()
        



pc_thread = threading.Thread(target=pc_func)
img_thread = threading.Thread(target=img_func)

pc_thread.start()
img_thread.start()

pc_thread.join()
img_thread.join()