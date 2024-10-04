import communication.config as Config
from communication.pc import PC
from communication.image_sender import ImageSender 
import threading
import time

pc = PC(Config.RPI_IP_ADDRESS, 5000) 
camera = ImageSender("tcp://192.168.32.27:5555")

def pc_func(pc):
    pc.connect()
    for i in range(4):
        pc.send("hi")
        time.sleep(2)

def camera_func(camera):
    for i in range(4):
        camera.takePic(1)
        time.sleep(2)


pc_thread = threading.Thread(target=pc_func, args=(pc,))
camera_thread = threading.Thread(target=camera_func, args=(camera,))

pc_thread.start()
camera_thread.start()

pc_thread.join()
camera_thread.join()



