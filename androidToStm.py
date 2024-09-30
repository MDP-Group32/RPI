from communication.android import Android, AndroidMessage
from communication.config import RPI_MAC_ADDRESS, PORT_NUMBER, SERIAL_PORT, BAUD_RATE
from communication.stm import STM

android = Android(RPI_MAC_ADDRESS, PORT_NUMBER)
android.connect()
message = android.receive()
print(message)

stm = STM(SERIAL_PORT, BAUD_RATE)
stm.connect()
stm.send(message)

android.disconnect()
stm.disconnect()
