#######################################################
# Modbus reading Python script.                       #
# More details in document                            #
# Modbus Map Versicharge Gen 3                        #
#######################################################
#
# 2023 achgut

# Read actual values in loop

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

    print("*" * separator)
    print("Reading data from Versicharge Wallbox: " + str(clientIP) + ":" + str(clientPort))
    print("-" * separator)
    print(">>> REAL-TIME VALUES Dynamic <<<")
    print("-" * separator)   

    # FW
    response = client.read_holding_registers(address=31,count=10,unit=UNIT)
    output = response.registers
    liste = list()
    for i in output:
        lower = i & 0b11111111
        upper = (i & 0b1111111100000000) >> 8
        liste.append(chr(upper))
        liste.append(chr(lower))
    strStatus = "FW: " + "".join(liste)
    print("-" * separator)   
    print(strStatus)
    print("-" * separator)   

    while True:  
      time.sleep(3)
      #Print Time info
      print("-" * separator)
      print(datetime.now())
      print("-" * separator)
    
      #Reg 1599 - EVSE State
      response = client.read_holding_registers(address=1599,count=1,unit=UNIT)
      print("EVSE State: " + str(response.registers[0]))
      
      #Reg 1600 - EVSE Error Code
      response = client.read_holding_registers(address=1600,count=1,unit=UNIT)
      print("EVSE Error Code: " + str(response.registers[0]))
    
      #Charger Status
      response = client.read_holding_registers(address=1601,count=1,unit=UNIT)
      strStatus = "Charger Status (OCPP State): " + str(response.registers[0])
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
    
  
      #Pausiert?
      response = client.read_holding_registers(address=1629,count=1,unit=UNIT)
      if(response.registers == [1]):
        strStatus = "Pause an : " + str(response.registers[0])
        print(strStatus)
      elif(response.registers == [2]):
        strStatus = "Pause aus : " + str(response.registers[0])
        print(strStatus)
      else:
        print("Pause nicht erkannt")  
      #MaxCurrent
      response = client.read_holding_registers(address=1633,count=1,unit=UNIT)
      print("Max Charging Current: " + str(response.registers[0]) + " A")
      #Current L1 - L3
      response = client.read_holding_registers(address=1647,count=4,unit=UNIT)
      strStatus = "Charging Current (L1 L2 L3 Sum): " + str(response.registers) + " A"
      print(strStatus)
     #Power L1 - L3
      response = client.read_holding_registers(address=1662,count=4,unit=UNIT)
      strStatus = "Charging Power (L1 L2 L3 Sum): " + str(response.registers) + " " + str(response.registers[3] / 10) + " W"
      print(strStatus)
    
    #Total Charing engery
      response = client.read_holding_registers(address=1692,count=2,unit=UNIT)
      output = response.registers
      zahl = output[0] << 16
      zahl |= output[1]
      zahl /= 10000.0
      strStatus = "Total Charging Energy (kWh): " + str(zahl) + "kWh"
      print(strStatus)
    
  except:
    print("-" * separator)
    print("An error has occurred during cluster data reading!")

if __name__ == "__main__":
  main()