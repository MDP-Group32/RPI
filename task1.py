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
android = Android(Config.RPI_MAC_ADDRESS, Config.BT_PORT_NUMBER)
stm = STM(Config.SERIAL_PORT, Config.BAUD_RATE)
pc = PC(Config.RPI_IP_ADDRESS, Config.RPI_PC_PORT)
camera = ImageSender(Config.PC_IP_ADDRESS)


android.connect()
print("Android connected")
stm.connect()
print("STM connected")
pc.connect()
print("PC connected")

#Receive obstacles from android
print("Waiting for obstacles from android...")
obstacles_json = android.receive()
print("Received obstacles from android...")

#Convert obstacles to dict and send to algo, to receive commands
obstacles_dict = json.loads(obstacles_json)
n_obstacles = str(len(obstacles_dict['obstacles']))

#send to pc
pc.send(n_obstacles)
print("Message sent: ", n_obstacles)
pc.disconnect()

#start a thread to connect to camera
camera.connect()
print("Camera Connected") 

commands_dict = get_stm_commands(obstacles_dict['obstacles']) 
commands = commands_dict["commands"]
print(type(commands))
print(commands)

#function to send commands to stm
def send_commands(commands):
    for command in commands:
        stm.send(command['value'])
        print("Command: ", command['value'])
        time.sleep(0.5)


#function to receive commands from stm
def stm_producer(p, buffer):
    while True:
        data = p.receive()
        buffer.put(data) 
        print("From STM: ",data)
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

#thread to receive commands from stm
stm_producer_thread = threading.Thread(target=stm_producer, args=(stm, stm_camera_buffer))

#thread to take pic when command is received
camera_consumer_thread = threading.Thread(target=camera_consumer, args=(camera, stm_camera_buffer))

send_commands(commands)

#TODO: Check if position is correct
print("Sending to android coordinates: ", commands_dict["coordinates"])
android.send(commands_dict["coordinates"])

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

#stm_send_thread.join()
stm_producer_thread.join()
print("Task 1 completed")