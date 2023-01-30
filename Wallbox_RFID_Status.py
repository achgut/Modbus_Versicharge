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
print("Reading data from Versicharge Wallbox: " + str(clientIP) + ":" + str(clientPort))
print("-" * separator)

#Charger Status
response = client.read_holding_registers(address=1601,count=1,unit=UNIT)
strStatus = "Charger Status: " + str(response.registers[0])
chargerstatus = response.registers[0]
print(strStatus)
if(response.registers == [1]):
  strStatus = "Charger Status: A (Power On)"
  print(strStatus)
elif(response.registers == [2]):
  strStatus = "Charger Status: B (Connected)" 
  print(strStatus)
elif(response.registers == [3]):
  strStatus = "Charger Status: C (Charging)" 
  print(strStatus)
elif(response.registers == [4]):
  strStatus = "Charger Status: C (Charging)" 
  print(strStatus)
elif(response.registers == [5]):
  responsepause = client.read_holding_registers(address=1629,count=1,unit=UNIT)
  if(responsepause.registers == [1]):
    strStatus = "Charger Status D und Pause an"
    print(strStatus)
  else:
    strStatus = "Charger Status D und keine Pause"
    print(strStatus)
else:
  print("Charging Fehler F")  
#RFID on?
response = client.read_holding_registers(address=79,count=1,unit=UNIT)
strStatus = "RFID Status: " + str(response.registers[0])
print(strStatus)
if(response.registers == [0]):
  strStatus = "RFID disabled" 
  print(strStatus)
elif(response.registers == [1]):
  strStatus = "RFID enabled" 
  print(strStatus)
else:
  print("RFID nicht erkannt")  
#Read RFID Erkennung
start = 338            # Anfangsregister
end = 339            # Enderegister +1
anzahl = 5

              # Anzahl der Bytes
helper = 0
print("-" * separator)  
while start < end :       
  response = client.read_holding_registers(address=start,count=anzahl) #,unit=UNIT) 
#
#   print(response)
  try: 
    strStatus = "Register " + str(start) + " (" + str(anzahl) + " Bytes RFID Karte erkannt): " 
    while helper < anzahl :   
      strStatus = strStatus + str(hex(response.registers[helper])) + " "
      helper += 1                                                         
    print(strStatus)
  except:
    print("Register " + str(start) + " :Error " + str(response)) 
  start += 1
  helper = 0

print("-" * separator)
print('Hello user Ende Abfrage')
