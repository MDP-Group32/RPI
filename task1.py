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

android.connect()
print("Android connected")
stm.connect()
print("STM connected")
pc.connect()
print("PC connected")

#pc must send its ip address and port to connect for camera, for now it is hardcoded
camera = ImageSender(Config.PC_IP_ADDRESS)
camera.connect()
print("Camera Connected") 

#Receive obstacles from android
print("Waiting for obstacles from android...")
obstacles_json = android.receive()
print("Received obstacles from android...")

#Convert obstacles to dict and send to algo, to receive commands
obstacles_dict = json.loads(obstacles_json)
n_obstacles = len(obstacles_dict['obstacles'])
n_obstacles_str = str(len(obstacles_dict['obstacles']))

#send to pc
pc.send(n_obstacles_str)
print("Message sent: ", n_obstacles_str)
pc.disconnect()

print("before get_stm_command")
commands_dict = get_stm_commands(obstacles_dict['obstacles']) 
print("after get_stm_command")

commands = commands_dict["path_string"]
commands_len = commands_dict['string_length']
print(type(commands))
print(commands)

#function to receive commands from stm
def producer(p, buffer):
    while True:
        data = p.receive()
        buffer.put(data) 
        print(f"From {p}:", data)
        if data == "#####":
            break

#function to send command to image rec
def camera_consumer(camera, buffer_consumer, android):
    while True:
        data = buffer_consumer.get()
        if data[0:2] == "ST":
            reply = camera.takePic(data[2:5]).decode("utf-8")
            print("Reply received from Image rec:", reply)
            android.send(reply)
            print("Sent to android", reply)
        else:
            camera.close() ##camera is disconnected
            break

#buffer stm_camera communication, pc_android communication
stm_camera_buffer = queue.Queue()

#thread to receive commands from stm
stm_producer_thread = threading.Thread(target=producer, args=(stm, stm_camera_buffer))

#thread to take pic when command is received, and send reply to android
camera_consumer_thread = threading.Thread(target=camera_consumer, args=(camera, stm_camera_buffer, android))

#send lengh of commands, then the command
stm.send(commands_len)
time.sleep(0.5)
stm.send(commands) ## double check, need send buffer size first then commands

stm_producer_thread.start()
camera_consumer_thread.start()


stm_producer_thread.join()
camera_consumer_thread.join()

android.disconnect()
stm.disconnect()

print("Task 1 completed")
