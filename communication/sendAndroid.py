from android import AndroidMessage, Android
from config import RPI_MAC_ADDRESS, PORT_NUMBER

android = Android(RPI_MAC_ADDRESS, PORT_NUMBER)
message = AndroidMessage("string", "f")
android.connect()
android.send(message)
android.disconnect()
