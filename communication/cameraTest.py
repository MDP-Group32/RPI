from camera import ImageAPI
from pc import PC
from config import RPI_IP_ADDRESS

pc = PC(RPI_IP_ADDRESS, 5000)

pc.connect()
camera = ImageAPI(pc.get_client_socket)
camera.takePic() #send to pc
pc.disconnect()