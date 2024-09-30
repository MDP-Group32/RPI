from communication.stm import STM
from communication.config import SERIAL_PORT, BAUD_RATE

#instantiate an object of STM class
stm = STM(SERIAL_PORT, BAUD_RATE)

#connect stm with respective baud rate and port
stm.connect()

#send message to stm
stm.send("F")
stm.disconnect()
#send command to stm