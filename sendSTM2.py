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

stm.send("s")
message = stm.receive()
print(message)
time.sleep(2)

stm.send("l")
message = stm.receive()
print(message)
time.sleep(2)

stm.send("r")

stm.disconnect()
 



