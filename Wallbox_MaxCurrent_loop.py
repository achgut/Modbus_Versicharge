#######################################################
# Modbus reading Python script.                       #
# More details in document                            #
# Modbus Map Versicharge Gen 3                        #
#######################################################
#
# 2023 achgut

# Set MaxCurrent 10A in a loop

#Imports
from pymodbus.client import ModbusTcpClient
import time
import sys
from datetime import datetime
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

def main(amp):
  try: 
    #Try to connect to client
    client = ModbusTcpClient(clientIP, clientPort) #Use port 502 for reading charger's data

    print("*" * separator)
    print("Reading data from Versicharge Wallbox: " + str(clientIP) + ":" + str(clientPort))
    print("-" * separator)
    print(">>> REAL-TIME VALUES Dynamic <<<")
    print("-" * separator)   
    print("-" * separator)
    print(datetime.now())
    print("Set to ", str(amp), " A")

    while True:  
      time.sleep(5)
      #Print Time info
      client.write_register(address=1633,value=int(amp),unit=UNIT)
   
   
  except:
    print("-" * separator)
    print("An error has occurred during cluster data reading!")

if __name__ == "__main__":
  main(sys.argv[1])