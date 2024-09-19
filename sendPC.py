from communication.pc import PC
from communication.config import RPI_IP_ADDRESS

pc = PC(RPI_IP_ADDRESS, 5000)

pc.connect()
pc.send("hi")
pc.disconnect()

