#######################################################
# Modbus reading Python script.                       #
# More details in document                            #
# Modbus Map Versicharge Gen 3                        #
#######################################################
#
# 2022 achgut

# Read salt

#Imports
from pymodbus.client import ModbusTcpClient
import time
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

def main():
  try: 
    #Try to connect to client
    client = ModbusTcpClient(clientIP, clientPort) #Use port 502 for reading charger's data
    time.sleep(2)
    
    #Print connection info
    print("*" * separator)
    print("Reading data from Versicharge Wallbox: " + str(clientIP) + ":" + str(clientPort))
    print("-" * separator)
    print(">>> REAL-TIME VALUES Dynamic <<<")
    print("-" * separator)
    print(datetime.now())
    print("-" * separator)
  
    # Salt

    helper = 0  
    response = client.read_holding_registers(address=1827,count=3) #,unit=UNIT) 
    try: 
      strStatus = "Salt: " 
      while helper < 3 :   
        strStatus = strStatus + str(hex(response.registers[helper])) + " "
        helper += 1                                                         
      print(strStatus)
    except:
      print("Register " + str(start) + " :Error " + str(response)) 
  
  except:
    print("-" * separator)
    print("An error has occurred during cluster data reading!")

if __name__ == "__main__":
  main()