from pc import PC
from config import RPI_IP_ADDRESS

pc = PC(RPI_IP_ADDRESS, 5000)

pc.connect()
pc.receive()
pc.disconnect()

