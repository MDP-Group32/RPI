from communication.image_sender import ImageSender
from communication.config import RPI_IP_ADDRESS
import communication.config as Config

camera = ImageSender(Config.PC_IP_ADDRESS) 
camera.takePic(1) #send to pc
