#######################################################
# Modbus reading Python script.                       #
# More details in document                            #
# Modbus Map Versicharge Gen 3  FW 2.118              #
#                                                     #
# Version 1.0                                         #
# 2022, achgut                                        #
#######################################################

#Imports
from pymodbus.client import ModbusTcpClient
import time
from datetime import datetime
from struct import *
from pymodbus.constants import Endian
from pymodbus.exceptions import ConnectionException
from pymodbus.payload import BinaryPayloadDecoder

#Initialisations
UNIT = 1
separator=80 #Separator line length
clientPort=502 #Port for modbus connection for reading charger's data

#PLEASE CHANGE CHARGER'S IP ADDRESS FIRST
################################################

clientIP="192.168.178.81" #PV's IP address

################################################

client = ModbusTcpClient(clientIP, clientPort) #Use port 502 for reading charger's data
response = client.read_holding_registers(address=1,count=1,unit=UNIT) 
if pymodbus.exceptions.ConnectionException :
    print ("Modbus Error: [Connection] Failed to connect[ModbusTcpClient(192.168.178.81:502)]")
else :
    print ("OK")


# #Special Read Register
# print("*" * separator)
# print("Reading data from Versicharge Wallbox: " + str(clientIP) + ":" + str(clientPort))
# print("-" * separator)
# print(">>> Registerabfragen nach Bereich <<<")
# print("*" * separator)
# 
# start = 1690              # Anfangsregister
# end = 1696                # Enderegister +1
# anzahl = 2                # Anzahl der Bytes
# helper = 0
# print("-" * separator)  
# while start < end :       
#   response = client.read_holding_registers(address=start,count=anzahl,unit=UNIT) 
#   try: 
#     strStatus = "Register " + str(start) + " (" + str(anzahl) + " Bytes): " 
#     while helper < anzahl :   
#       strStatus = strStatus + " : " + str(response.registers[helper])
#       helper += 1                                                         
#     print(strStatus)
#   except:
#     print("Register " + str(start) + " :Error") 
#   start += 1
#   helper = 0
#  
# print('Hello user Ende Abfrage')
# 