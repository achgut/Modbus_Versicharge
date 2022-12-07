#######################################################
# Modbus reading Python script.                       #
# More details in document                            #
# Modbus Map Versicharge Gen 3  FW 2.118              #
#                                                     #
# Version 1.0                                         #
# 2022, achgut                                        #
#######################################################

# Neu: 1601 -> Status Charger nicht dokumentiert
# Fehler 23 Slave Failure 131,3 -> UTC Zeit Reg
# Fehler: 1660, 1661 Illegal Adress 131,3 -> sind aber Failback Regs
# Fehler: 1852 - 1877 Illegal Adress 131,3 -> sind aber AdminWhitelist Regs
# Neu: 959, 960: 129,1,Illegal Funktion -> WO?
#
#Imports
from pymodbus.client import ModbusTcpClient
import pymodbus.exceptions
import time
from datetime import datetime
from struct import *
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
# import Wallbox_read_Static
# import Wallbox_read_Actual

#Initialisations
UNIT = 1
separator=80 #Separator line length
clientPort=502 #Port for modbus connection for reading charger's data

#PLEASE CHANGE CHARGER'S IP ADDRESS FIRST
################################################

clientIP="192.168.178.63" #Charger's IP address

################################################

client = ModbusTcpClient(clientIP, clientPort) #Use port 502 for reading charger's data

# Wallbox_read_Static
# Wallbox_read_Actual

print("-" * separator)

#Special Read Register
print("*" * separator)
print("Reading data from Versicharge Wallbox: " + str(clientIP) + ":" + str(clientPort))
print("-" * separator)
print(">>> Registerabfragen nach Bereich <<<")
print("*" * separator)

start = 80             # Anfangsregister
end = 87            # Enderegister +1
anzahl = 1               # Anzahl der Bytes
helper = 0
print("-" * separator)  
while start < end :       
  response = client.read_holding_registers(address=start,count=anzahl) #,unit=UNIT) 
#
#   print(response)
  try: 
    strStatus = "Register " + str(start) + " (" + str(anzahl) + " Bytes): " 
    while helper < anzahl :   
      strStatus = strStatus + " : " + str(response.registers[helper])
      helper += 1                                                         
    print(strStatus)
  except:
    print("Register " + str(start) + " :Error " + str(response)) 
  start += 1
  helper = 0

## RFID HEX READ
#anzahl = 1
#reg = 86
#while anzahl < 3 :
#  response = client.read_holding_registers(address=reg,count=anzahl,unit=UNIT)
#  print(response)
#  output = response.registers
#  zahl = output[3] << 16
#  zahl |= output[4]
#  strStatus = "RFID Whitelist UID RFID " + str(count) + ": " + str(hex(zahl))
#  print(strStatus)
#  anzahl += 1
#  reg += 5
#
print('Hello user Ende Abfrage')
