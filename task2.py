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


message = android.receive()
stm.send(message)


