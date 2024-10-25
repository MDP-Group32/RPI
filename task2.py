#communication modules
from communication.algo import get_stm_commands
from communication.android import Android
from communication.stm import STM
from communication.pc import PC
import communication.config as Config
from communication.image_sender import ImageSender

#functional modules
import threading
import time
import queue
import json

android = Android(Config.RPI_MAC_ADDRESS, Config.BT_PORT_NUMBER)
stm = STM(Config.SERIAL_PORT, Config.BAUD_RATE)
camera = ImageSender(Config.PC_IP_ADDRESS)

android.connect()
print("Android Connected")

stm.connect()
print("STM Connected")

camera.connect()
print("Camera Connected")

#producer and consumer functions for threads
def producer(p, buffer):
    while True:
        data = p.receive()
        buffer.put(data) 
        print(f"From {p}:", data)
        if data == "#####":
            break

def camera_consumer(camera, buffer, stm):
    count = 1
    while True:
        data = buffer.get()
        if count < 3: 
            reply = camera.takePic(count).decode("utf-8")
            print("Reply received from Image rec:", reply)
            stm.send('l')
            print("Sent to STM: ", 'l')
            count+=1
        else:
            camera.close() ##camera is disconnected
            break


stm_camera_buffer = queue.Queue()

#thread to receive capture commands from stm
stm_producer_thread = threading.Thread(target=producer, args=(stm, stm_camera_buffer))

#thread to take pic
camera_consumer_thread = threading.Thread(target=camera_consumer, args=(camera, stm_camera_buffer, android))


#receive start command from android then send to stm
message = android.receive()
print("Message from Android: ", message)

stm_producer_thread.start()
camera_consumer_thread.start()
stm.send('s')

#stm_producer_thread().join()
#camera_consumer_thread.join()

print("Task 2 completed")

