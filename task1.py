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

#initiate and connect android, camera,stm modules
android = Android(Config.RPI_MAC_ADDRESS, Config.PORT_NUMBER)
stm = STM(Config.SERIAL_PORT, Config.BAUD_RATE)
camera = ImageSender("tcp://192.168.32.27:5555")

camera.connect()
print("Camera Connected") 
android.connect()
print("Android connected")
stm.connect()
print("STM connected")

#Receive obstacles from android
obstacles_json = android.receive()

#Convert obstacles to dict and send to algo, to receive commands
obstacles_dict = json.loads(obstacles_json)
commands_dict = get_stm_commands(obstacles_dict['obstacles']) 
commands = commands_dict["commands"]

#function to send commands to stm
def send_commands(commands):
    for command in commands:
        stm.send(command['value'])
        print("Command: ", command['value'])
        time.sleep(1)

#function to receive commands from stm
def stm_producer(p, buffer):
    while True:
        data = p.receive()
        buffer.put(data) 
        if data == "#####":
            break

#function to send command to image rec
def camera_consumer(camera, buffer):
    while True:
        data = buffer.get()
        if data[0:2] == "ST":
            camera.takePic(data[2:5])
        else:
            camera.close()
            break

#buffer to receive commands from stm
stm_camera_buffer = queue.Queue()

#thread to send commands to stm
stm_send_thread = threading.Thread(target=send_commands, args=(commands))

#thread to receive commands from stm
stm_producer_thread = threading.Thread(target=stm_producer, args=(stm, stm_camera_buffer))

#thread to take pic when command is received
camera_consumer_thread = threading.Thread(target=camera_consumer, args=(camera, stm_camera_buffer))

stm_send_thread.start()
stm_producer_thread.start()
camera_consumer_thread.start()

camera_consumer_thread.join()

#connect to pc after camera connection is closed
pc = PC(Config.RPI_IP_ADDRESS, 5000)
pc.connect()

#receive image content from pc, then send to android
image_content = pc.receive()
android.send(image_content)

#close connections
pc.disconnect()
android.disconnect()

stm_send_thread.join()
stm_producer_thread.join()