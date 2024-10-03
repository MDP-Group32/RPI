from communication.pc import PC
import communication.config as Config
from communication.image_sender import ImageSender
from communication.android import Android
import time

pc = PC(Config.RPI_IP_ADDRESS, 5000)
android = Android(Config.RPI_MAC_ADDRESS, Config.PORT_NUMBER)

pc.connect()
pc.send("2")
pc.disconnect()

camera = ImageSender("tcp://192.168.32.27:5555")
camera.connect()
camera.takePic(1)
time.sleep(1)
camera.takePic(2)
time.sleep(1)

pc.connect()
message = pc.receive()
print(message)

android.connect()
android.send(message)
android.disconnect()





