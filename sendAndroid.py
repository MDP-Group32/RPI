from communication.android import Android
from communication.config import RPI_MAC_ADDRESS, BT_PORT_NUMBER

android = Android(RPI_MAC_ADDRESS, BT_PORT_NUMBER)
message = "hi"
android.connect()
android.send(message)
android.disconnect()
