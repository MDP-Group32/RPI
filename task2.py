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
stm.connect()
camera.connect()

#receive start command from android then send to stm
message = android.receive()
stm.send(message)

#function to send command to image rec
def camera_cnp(camera, buffer_consumer, buffer_producer):
    while True:
        data = buffer_consumer.get()
        if data[0:2] == "ST":
            reply = camera.takePic(data[2:5])
            buffer_producer.put(reply)
        else:
            camera.close() ##camera is disconnected
            break





