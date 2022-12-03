#######################################################
# Modbus reading Python script.                       #
# More details in document                            #
# Modbus Map Versicharge Gen 3                        #
#                                                     #
# Version 1.0                                         #
# November, 2022                                       #
# Author: Achim                                       #
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
try:
    #Try to connect to client
    client = ModbusTcpClient(clientIP, clientPort) #Use port 502 for reading charger's data

     #1 oder 3 Phasiges Laden?
    response = client.read_holding_registers(address=1642,count=1,unit=UNIT)
    if(response.registers == [0]):
      strStatus = "1 Phasiges Laden " + str(response.registers[0])
      print(strStatus)
    elif(response.registers == [1]):
      strStatus = "3 Phasiges Laden " + str(response.registers[0])
      print(strStatus)
    else:
      print("Phase nicht erkannt")  

    if(response.registers == [0]):
      client.write_register(address=1642,value=1,unit=UNIT)
      strStatus = "Auf 3 Phasig umschalten "
      print(strStatus)
     
    else:  
      client.write_register(address=1642,value=0,unit=UNIT)
      strStatus = "Auf 1 Phasig umschalten  "
      print(strStatus)
   
    response = client.read_holding_registers(address=1642,count=1,unit=UNIT)
    if(response.registers == [0]):
      strStatus = "1 Phasiges Laden " + str(response.registers[0])
      print(strStatus)
    elif(response.registers == [1]):
      strStatus = "3 Phasiges Laden " + str(response.registers[0])
      print(strStatus)
    else:
      print("Phase nicht erkannt")  

except:
    print("-" * separator)
    print("An error has occurred during cluster data reading!")

