from stm import STM

#instantiate an object of STM class
stm = STM()

#connect stm with respective baud rate and port
stm.connect()

#receive message from stm
str = stm.waitReceive()
print(str)
stm.disconnect()
