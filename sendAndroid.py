from communication.android import Android
from communication.config import RPI_MAC_ADDRESS, PORT_NUMBER

android = Android(RPI_MAC_ADDRESS, PORT_NUMBER)
message = "hi"
android.connect()
android.send(message)
android.disconnect()
