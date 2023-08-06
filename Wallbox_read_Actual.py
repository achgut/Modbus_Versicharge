#######################################################
# Modbus reading Python script.                       #
# More details in document                            #
# Modbus Map Versicharge Gen 3                        #
#######################################################
#
# 2022 achgut

#
#************************************************************************************
#
# Verwendete Versicharge GEN 3:
#// Versicharge GEN3 FW2.118 oder höher
#// Commercial Version (Reg 22 = 2), One Outlet: (Reg 24 = 1)
#// Integrated MID (Reg 30 = 4)
#// Order Number: 8EM1310-3EJ04-0GA0
#
#//https://support.industry.siemens.com/cs/attachments/109814359/versicharge_wallbox_modBus_map_en-US-FINAL.pdf
#
#// Gefundene Fehler:
#  // Status Wallbox (A-F): Register 1601 nicht im ModbusMap dokumentiert. 
#  // Active Power Phase Sum wird bei Strömen über 10A falsch berechnet (Register 1665)
#  // Minimal Current: Muss als 7A eingestellt werden. Regelung dann auf 6A.
#  // Phasenumschaltung funktioniert nicht - Läd immmer mit 3 Phasen teilweise Absturz Wallbox

# Update FW 1.120:
# Fallback Settings (Reg 1660/1661) funktionieren (lesbar)
#************************************************************************************

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
    time.sleep(2)
    #Try to connect to client
    client = ModbusTcpClient(clientIP, clientPort) #Use port 502 for reading charger's data
    connection = client.connect()

    #Print connection info
    print("*" * separator)
    print("Reading data from Versicharge Wallbox: " + str(clientIP) + ":" + str(clientPort))
    print("-" * separator)
    print(">>> REAL-TIME VALUES Dynamic <<<")
    print("-" * separator)
    print(datetime.now())
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
    print(strStatus)

    #Temperature PCB
    response = client.read_holding_registers(address=1602,count=1,unit=UNIT)
    t = response.registers[0]
    if t > 65000 :
      t = t - 65536
    strStatus = "Temperatur PCB: " + str(t) + "°C"
    print(strStatus)


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
      responseMaxCurrent = client.read_holding_registers(address=1633,count=1,unit=UNIT)
      if(responseMaxCurrent.registers == 0):
        strStatus = "Charger Status D und Pause an"
        print(strStatus)
      else:
        strStatus = "Charger Status D und keine Pause"
        print(strStatus)
    else:
      print("Charging Fehler F")  
  
    #Charger Delay
    response = client.read_holding_registers(address=26,count=1,unit=UNIT)
    print("Charger Delay: " + str(response.registers[0]))
      
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

    # RFID Karte erkannt
    helper = 0  
    response = client.read_holding_registers(address=338,count=5) #,unit=UNIT) 
    try: 
      strStatus = "RFID Karte: " 
      while helper < 5 :   
        strStatus = strStatus + str(hex(response.registers[helper])) + " "
        helper += 1                                                         
      print(strStatus)
    except:
      print("Register " + str(338) + " :Error " + str(response)) 

    #MaxCurrent
    response = client.read_holding_registers(address=1633,count=1,unit=UNIT)
    print("Max Charging Current: " + str(response.registers[0]) + " A")
  
    #Pausiert?
    response = client.read_holding_registers(address=1633,count=1,unit=UNIT)
    if(response.registers == [0]):
      strStatus = "Pause an : " + str(response.registers[0])
      print(strStatus)
    else:
      strStatus = "Pause aus : " + str(response.registers[0])
      print(strStatus)
 
    #1 oder 3 Phasig
    response = client.read_holding_registers(address=1642,count=1,unit=UNIT)
    if(response.registers == [1]):
      strStatus = "Phases for Charging: 3 Phasen" 
      print(strStatus)
    elif(response.registers == [0]):
      strStatus = "Phases for Charging: 1 Phase" 
      print(strStatus)
    else:
      print("Phase nicht erkannt")  
    #Current L1 - L3
    response = client.read_holding_registers(address=1647,count=4,unit=UNIT)
    strStatus = "Charging Current (L1 L2 L3 Sum): " + str(response.registers) + " A"
    print(strStatus)
    #Voltage L1 - L3
    response = client.read_holding_registers(address=1651,count=3,unit=UNIT)
    strStatus = "Charging Voltage (L1 L2 L3): " + str(response.registers) + " V zu N"
    print(strStatus)
    #Power L1 - L3
    response = client.read_holding_registers(address=1662,count=4,unit=UNIT)
    strStatus = "Charging Power (L1 L2 L3 Sum): " + str(response.registers) + " W"
    print(strStatus)
    #Apparent Power L1 - L3
    response = client.read_holding_registers(address=1670,count=4,unit=UNIT)
    strStatus = "Apparent Power (L1 L2 L3 Sum): " + str(response.registers) + " VA"
    print(strStatus)
    #Reactive Power L1 - L3
    response = client.read_holding_registers(address=1674,count=4,unit=UNIT)
    helper = 0
    strStatus = "Reactive Power (L1 L2 L3 Sum): "  
    while helper < 4 :   
      RP = int(response.registers[helper]) 
      if (RP & (1 << (16 - 1))) != 0:
        RP = RP - (1 << 16)
      helper += 1     
      strStatus = strStatus + str(RP) + " "
    strStatus = strStatus + "VA Reactive Power"
    print(strStatus)
    #Power Factor L1 - L3
    response = client.read_holding_registers(address=1666,count=4,unit=UNIT)
    strStatus = "Power Factor (L1 L2 L3 Sum): " + str(response.registers[0] / 1000) + " " + str(response.registers[1] / 1000) + " "  + str(response.registers[2] / 1000) + " "  + str(response.registers[3] / 1000) + " "
    print(strStatus)
    #Failsafe Settings Current
    response = client.read_holding_registers(address=1660,count=1,unit=UNIT) # Register 1660 !!!!
    strStatus = "Fallback Current: " + str(response.registers[0]) + "A"
    print(strStatus)
    #Failsafe Settings Time
    response = client.read_holding_registers(address=1661,count=2,unit=UNIT) # Register 1661 !!!!
    strStatus = "Fallback Time: " + str(response.registers[0]) + "s"
    print(strStatus)
  #Total Charing engery
    response = client.read_holding_registers(address=1692,count=2,unit=UNIT)
    output = response.registers
    zahl = output[0] << 16
    zahl |= output[1]
    zahl /= 10000.0
    strStatus = "Total Charging Energy (kWh): " + str(zahl) + "kWh"
    print(strStatus)
    client.close()

  except:
    print("-" * separator)
    print("An error has occurred during cluster data reading!")

if __name__ == "__main__":
  main()