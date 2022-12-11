#######################################################
# Modbus reading Python script.                       #
# More details in document                            #
# Modbus Map Versicharge Gen 3                        #
#                                                     #
# Version 1.0                                         #
# November, 2022                                      #
# Author: Achim         achgut                        #
#######################################################

#Imports
from pymodbus.client import ModbusTcpClient
import datetime
from struct import *
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

#Initialisations
UNIT = 1
separator=80 #Separator line length
clientPort=502 #Port for modbus connection for reading charger's data

#PLEASE CHANGE CHARGER'S IP ADDRESS FIRST
################################################

clientIP="192.168.178.63" #Charger's IP address

################################################

# Read data
# Charger data
def main():
  try:
    #Try to connect to client
    client = ModbusTcpClient(clientIP, clientPort) #Use port 502 for reading charger's data

     #Pausiert?
    response = client.read_holding_registers(address=1629,count=1,unit=UNIT)
    if(response.registers == [1]):
      strStatus = "Pause an " + str(response.registers[0])
      print(strStatus)
    elif(response.registers == [2]):
      strStatus = "Pause aus " + str(response.registers[0])
      print(strStatus)
    else:
      print("Pause nicht erkannt")  

    if(response.registers == [1]):
      client.write_register(address=1629,value=2,unit=UNIT)
      strStatus = "Pause ausschalten "
      print(strStatus)
     
    else:  
      client.write_register(address=1629,value=1,unit=UNIT)
      strStatus = "Pause einschalten "
      print(strStatus)
   
    response = client.read_holding_registers(address=1629,count=1,unit=UNIT)
    if(response.registers == [1]):
      strStatus = "Pause an " + str(response.registers[0])
      print(strStatus)
    elif(response.registers == [2]):
      strStatus = "Pause aus " + str(response.registers[0])
      print(strStatus)
    else:
      print("Pause nicht erkannt")        

  except:
    print("-" * separator)
    print("An error has occurred during cluster data reading!")


if __name__ == "__main__":
  main()