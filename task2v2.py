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

#receive start command from android then send to stm
message = android.receive()
print("Message from Android: ", message)
stm.send('s')




count = 1
while True:
    stm.receive()
    reply = camera.takePic(count).decode('utf-8')
    print("Reply type:", type(reply))
    print("Reply: ", reply)
    stm.send(reply) #check if reply is a string
    count+=1
    if(count > 2):
        break

print("Task 2 completed")

