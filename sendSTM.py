from communication.stm import STM
from communication.config import SERIAL_PORT, BAUD_RATE
import time
import threading
import queue

def send_commands():
    stm.send("FL000")
    time.sleep(0.5)

    stm.send("FF100")
    time.sleep(0.5)

    stm.send("ST000")
    time.sleep(0.5)
    
    stm.send("RR100")
    time.sleep(0.5)

    stm.send("BL000")
    time.sleep(0.5)

    stm.send("#####")
    time.sleep(0.5)

def producer(p, buffer):
    while True:
        command = p.receive()
        buffer.put(command)
        print("Producer: ", command)

# def consumer(buffer):
#     while True:
#         message = buffer.get()
#         print("Consumer:", message)
#         if message == "ST000":
#             break


buffer = queue.Queue()

#instantiate an object of STM class
stm = STM(SERIAL_PORT, BAUD_RATE)

#connect stm with respective baud rate and port
stm.connect()

#Thread to send and receive from stm
stm_send_thread = threading.Thread(target=send_commands)
producer_thread = threading.Thread(target=producer, args=(stm, buffer))
# consumer_thread = threading.Thread(target=consumer, args=(buffer))

stm_send_thread.start()
producer_thread.start()
# consumer_thread.start()

stm_send_thread.join()
print("stm_send_thread completed")

producer_thread.join()
# consumer_thread.join()

stm.disconnect()
 



# for i in range(len(command)):
#     stm.send(command[i])
