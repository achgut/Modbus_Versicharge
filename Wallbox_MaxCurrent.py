#######################################################
# Modbus writing Python script.                       #
# Set Max Charging Current                            #
# 1 Int als Argument mitgeben                         #
#                                                     #
# Modbus Map Versicharge Gen 3                        #
#                                                     #
# Version 1.0                                         #
# November, 2022                                      #
# Author: Achim            achgut                     #
#######################################################

#Imports
from pymodbus.client import ModbusTcpClient
import datetime
import sys
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

def main(amp):
    try:
      #Try to connect to client
      client = ModbusTcpClient(clientIP, clientPort) #Use port 502 for reading charger's data
       #MaxCurrent?
      response = client.read_holding_registers(address=1633,count=1,unit=UNIT)
      strStatus = "Max Current: " + str(response.registers[0]) + "A"
      print(strStatus)
      print("Set to ", str(amp), " A")
      client.write_register(address=1633,value=int(amp),unit=UNIT)
    
      response = client.read_holding_registers(address=1633,count=1,unit=UNIT)
      strStatus = "Max Current: " + str(response.registers[0]) + "A"
      print(strStatus)
    except:
      print("-" * separator)
      print("An error has occurred during cluster data reading!")
      
if __name__ == "__main__":
    main(sys.argv[1])