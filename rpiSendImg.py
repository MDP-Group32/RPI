from communication.image_sender import ImageSender
from communication.config import RPI_IP_ADDRESS

camera = ImageSender("tcp://192.168.32.27:5555") 
camera.takePic(1) #send to pc
