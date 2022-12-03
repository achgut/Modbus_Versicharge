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

    # Reboot
    
    client.write_register(address=1826,value=1,unit=UNIT)
    
except:
    print("-" * separator)
    print("An error has occurred during cluster data reading!")

