#communication modules
from communication.algo import get_stm_commands
from communication.android import Android
from communication.stm import STM
from communication.pc import PC
import communication.config as Config

#functional modules
import threading
import time
import queue
import json

#initiate all modules
android = Android(Config.RPI_MAC_ADDRESS, Config.PORT_NUMBER)


pc = PC(Config.RPI_IP_ADDRESS, 5000)


stm = STM(Config.SERIAL_PORT, Config.BAUD_RATE)

android_connect_thread = threading.Thread(target=android.connect)
pc_connect_thread = threading.Thread(target=pc.connect)
stm_connect_thread = threading.Thread(target=stm.connect)

#Start connections of modules
android_connect_thread.start()
pc_connect_thread.start()
stm_connect_thread.start()

#wait for all modules to be connected before proceeding
#connection errors are handled in the respective modules
android_connect_thread.join()
pc_connect_thread.join()
stm_connect_thread.join()
print("All connections successful")

#android sends obstacles to rpi, which will be sent to algo (json object)
#indicates start
obstacles = android.receive()
# pc.send(obstacles)

commands_object_json = get_stm_commands(obstacles)
print('Commands object json:', commands_object_json)

#algo sends all commands(hamiltonian path) to rpi, convert to python dictionary
# commands_object_json = pc.receive()#calling local host


commands_dict = json.loads(commands_object_json)
print('Commands dict:', commands_dict)

#put commands in a queue
commands_queue = queue.Queue()
for command in commands_dict["commands"]:
    #parse the command and put in queue
    commands_queue.put(command)

#function to read data from pc to put into queue
def producer(p, buffer):
    while True:
        data = p.receive()
        buffer.put(data) 

#function to send data to android from queue
def consumer(c, buffer):
    while True:
        data = buffer.get()
        c.send(data)#data needs to be Android/jsonified?


#buffer(producer-consuemr) from image rec to send image content to android
pc_android_buffer = queue.Queue()
producer_thread = threading.Thread(target=producer, args=(pc, pc_android_buffer))
consumer_thread = threading.Thread(target=consumer, args=(android, pc_android_buffer))

#should this be a thread?
#send commands to stm
def sendCommand(queue,stm):
    while not queue.empty():
        command = queue.get().value
        stm.send(command)


#thread to send commands to stm
command_thread = threading.Thread(target=sendCommand, args=(commands_queue, stm))

producer_thread.join()
consumer_thread.join()
command_thread.join()


























