from communication.stm import STM
from communication.config import SERIAL_PORT, BAUD_RATE
import time
import threading
import queue

#instantiate an object of STM class
print(SERIAL_PORT, BAUD_RATE)
stm = STM(SERIAL_PORT, BAUD_RATE)

#connect stm with respective baud rate and port
stm.connect()

stm.send("FF100")
time.sleep(0.5)
stm.send("#####")

stm.disconnect()
 



