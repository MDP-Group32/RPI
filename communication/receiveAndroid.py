from android import Android, AndroidMessage
from config import RPI_MAC_ADDRESS, PORT_NUMBER

android = Android(RPI_MAC_ADDRESS, PORT_NUMBER)
android.connect()
message = android.receive()
android.disconnect()
print(message)
