from stm import STM

#instantiate an object of STM class
stm = STM()

#connect stm with respective baud rate and port
stm.connect()

#send message to stm
stm.send("f")
stm.disconnect()
#send command to stm