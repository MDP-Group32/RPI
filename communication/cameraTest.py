from camera import ImageAPI
from pc import PC
from config import RPI_IP_ADDRESS

pc = PC(RPI_IP_ADDRESS, 5000)

pc.connect()

remote_ip, remote_port = pc.get_client_socket().getpeername()
print("ip: ", remote_ip)
print("port: ", remote_port)
camera = ImageAPI(f"tcp://{remote_ip}:{remote_port}") #"tcp://192.168.32.14:5555"
camera.takePic() #send to pc
pc.disconnect()