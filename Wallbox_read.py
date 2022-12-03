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

# Read data
# Charger data
try:
    #Try to connect to client
    client = ModbusTcpClient(clientIP, clientPort) #Use port 502 for reading charger's data

    #Print connection info
    print("*" * separator)
    print("Reading data from Versicharge Wallbox: " + str(clientIP) + ":" + str(clientPort))
    print("-" * separator)
    print(">>> REAL-TIME VALUES <<<")
    print("*" * separator)

    #Reading INPUT REGISTERS
    print("-" * separator)
    print(">>> Charger Specification <<<")
    print("-" * separator)

    #Manufacturer
    response = client.read_holding_registers(address=0,count=5,unit=UNIT)
    
    output = response.registers
    liste = list()
    for i in output:
        lower = i & 0b11111111
        upper = (i & 0b1111111100000000) >> 8
        liste.append(chr(upper))
        liste.append(chr(lower))
    
    strStatus = "Manufacturer: " + "".join(liste)
    print(strStatus)

    # Serial
    response = client.read_holding_registers(address=7,count=5,unit=UNIT)
    
    output = response.registers
    liste = list()
    for i in output:
        lower = i & 0b11111111
        upper = (i & 0b1111111100000000) >> 8
        liste.append(chr(upper))
        liste.append(chr(lower))
    
    strStatus = "Seriennummer: " + "".join(liste)
    print(strStatus)

    # Order Number
    response = client.read_holding_registers(address=12,count=10,unit=UNIT)
    
    output = response.registers
    liste = list()
    for i in output:
        lower = i & 0b11111111
        upper = (i & 0b1111111100000000) >> 8
        liste.append(chr(upper))
        liste.append(chr(lower))
    strStatus = "Order Number: " + "".join(liste)
    print(strStatus)
    
    # Production Date
    response = client.read_holding_registers(address=5,count=2,unit=UNIT)
    output = response.registers
    liste = list()
    for i in output:
        lower = i
        liste.append(str(lower))
    strStatus = "Production Date: " + str(liste[1][0:2]) + "." +str(liste[1][2:4]) + "." + str(liste[0])
    print(strStatus)

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

    # Modbustable
    response = client.read_holding_registers(address=41,count=1,unit=UNIT)
    strStatus = "Modbus Table: " + str(response.registers[0])
    print(strStatus) 

   # Plattform Type (2:Commercial)
    response = client.read_holding_registers(address=22,count=1,unit=UNIT)
    strStatus = "Platform Type (2 = Commercial): " + str(response.registers[0])
    print(strStatus) 

   # Meter Type
    response = client.read_holding_registers(address=30,count=1,unit=UNIT)
    strStatus = "Meter (4=Integrated meter MID): " + str(response.registers[0])
    print(strStatus) 

  # Connectivity Charger
    response = client.read_holding_registers(address=27,count=1,unit=UNIT)
    strStatus = "Connectivity Charger (3=Cellular -> Falsch): " + str(response.registers[0])
    print(strStatus)   
    
  # Outlets
    response = client.read_holding_registers(address=24,count=1,unit=UNIT)
    strStatus = "Anzahl Outlets: " + str(response.registers[0])
    print(strStatus) 
           
    # Rated Current
    response = client.read_holding_registers(address=28,count=2,unit=UNIT)
    strStatus = "Rated Current: " + str(response.registers[0]) + "A"
    print(strStatus)
    strStatus = "Current DIP Switch: " + str(response.registers[1]) + "A"
    print(strStatus)
  
    print("-" * separator)
    print(">>> RFID Status <<<")
    print("-" * separator)

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

# RFID Whitelist
    response = client.read_holding_registers(address=87,count=1,unit=UNIT)
    strStatus = "RFID Whitelist Anzahl: " + str(response.registers[0])
    print(strStatus)

# RFID UID 0
    response = client.read_holding_registers(address=88,count=5,unit=UNIT)
    output = response.registers
    zahl = output[3] << 16
    zahl |= output[4]
    strStatus = "RFID Whitelist UID RFID 0: " + str(hex(zahl))
    print(strStatus)
# RFID UID 1
    response = client.read_holding_registers(address=93,count=5,unit=UNIT)
    output = response.registers
    zahl = output[3] << 16
    zahl |= output[4]
    strStatus = "RFID Whitelist UID RFID 1 (Florian i3): " + str(hex(zahl))
    print(strStatus)
# RFID UID 2
    response = client.read_holding_registers(address=98,count=5,unit=UNIT)
    output = response.registers
    zahl = output[3] << 16
    zahl |= output[4]
    strStatus = "RFID Whitelist UID RFID 2: " + str(hex(zahl))
    print(strStatus)

    print("-" * separator)
    print(">>> Charger Status <<<")
    print("-" * separator)

    #Temperature PCB
    response = client.read_holding_registers(address=1602,count=1,unit=UNIT)
    strStatus = "Temperatur PCB: " + str(response.registers[0]) + "°C"
    print(strStatus)

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
    else:
      print("Charging Fehler D oder F")  

   #Charger Delay
    response = client.read_holding_registers(address=26,count=1,unit=UNIT)
    if(response.registers == [0]):
      strStatus = "Charger Delay: No Delay"
      print(strStatus)
    elif(response.registers == [1]):
      strStatus = "Charger Delay: 2h Delay"
      print(strStatus)
    elif(response.registers == [2]):
      strStatus = "Charger Delay: 4h Delay"
      print(strStatus)
    elif(response.registers == [3]):
      strStatus = "Charger Delay: 6h Delay" 
      print(strStatus)
    elif(response.registers == [4]):
      strStatus = "Charger Delay: 8h Delay"  
      print(strStatus)
    else:
      print("Charging Fehler D oder F")  

    print("-" * separator)
    print(">>> Actual Data <<<")
    print("-" * separator)

    #MaxCurrent
    response = client.read_holding_registers(address=1633,count=1,unit=UNIT)
    Currentstatus = response.registers[0]
    strStatus = "Max Current: " + str(response.registers[0]) + "A"
    print(strStatus)

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
    strStatus = "Charging Power (L1 L2 L3 Sum): " + str(response.registers) + " " + str(response.registers[3] / 10) + " W"
    print(strStatus)
#Power Factor L1 - L3
    response = client.read_holding_registers(address=1666,count=4,unit=UNIT)
    strStatus = "Power Factor (L1 L2 L3 Sum): " + str(response.registers[0] / 100) + " " + str(response.registers[1] / 100) + " "  + str(response.registers[2] / 100) + " "  + str(response.registers[3] / 100) + " "
    print(strStatus)
#Apparent Power L1 - L3
    response = client.read_holding_registers(address=1670,count=4,unit=UNIT)
    strStatus = "Apparent Power (L1 L2 L3 Sum): " + str(response.registers) + " VA"
    print(strStatus)
#Reactive Power L1 - L3
    response = client.read_holding_registers(address=1674,count=4,unit=UNIT)
    strStatus = "Reactive Power (L1 L2 L3 Sum): " + str(response.registers) + " VA reactive"
    print(strStatus)
#Total Charing engery
    response = client.read_holding_registers(address=1692,count=2,unit=UNIT)
    output = response.registers
    zahl = output[0] << 16
    zahl |= output[1]
    zahl /= 10.0

    strStatus = "Total Charging Energy (kWh): " + str(zahl) + "kWh"
    print(strStatus)

except:
    print("-" * separator)
    print("An error has occurred during cluster data reading!")

####################################################################################################################
var = 1
try:
  while True :
    print("-" * separator)
    print("Loop " , var, datetime.now())
    time.sleep(2)
    var += 1
  #Temperature PCB
    response = client.read_holding_registers(address=1602,count=1,unit=UNIT)
    print("Temperatur PCB: " + str(response.registers[0]) + "°C")
  #Charger Status
    response = client.read_holding_registers(address=1601,count=1,unit=UNIT)
    if (response.registers[0] == chargerstatus):
      print("Charger Status: " + str(response.registers[0]))
    else:
      print("\33[2;31;43mCharger Status: " + str(response.registers[0]) + "\33[0;37;40m")   
    chargerstatus = response.registers[0]
  #Charger Delay
    response = client.read_holding_registers(address=26,count=1,unit=UNIT)
    print("Charger Delay: " + str(response.registers[0]))
  #MaxCurrent
    response = client.read_holding_registers(address=1633,count=1,unit=UNIT)
    if (response.registers[0] == Currentstatus):
      print("Max Charging Current: " + str(response.registers[0]) + " A" + "\33[0;37;40m")
    else:
      print("\33[2;31;43mMax Charging Current : " + str(response.registers[0]) + " A" + "\33[0;37;40m")   
    Currentstatus = response.registers[0]  
  
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
    strStatus = "Charging Power (L1 L2 L3 Sum): " + str(response.registers) + " " + str(response.registers[3] / 10) + " W"
    print(strStatus)
  #Apparent Power L1 - L3
    response = client.read_holding_registers(address=1670,count=4,unit=UNIT)
    strStatus = "Apparent Power (L1 L2 L3 Sum): " + str(response.registers) + " VA"
    print(strStatus)
  #Total Charing engery
    response = client.read_holding_registers(address=1692,count=2,unit=UNIT)
    output = response.registers
    zahl = output[0] << 16
    zahl |= output[1]
    zahl /= 10.0

    strStatus = "Total Charging Energy (kWh): " + str(zahl) + "kWh"
    print(strStatus)

except KeyboardInterrupt:
  print('Hello user you have pressed ctrl-c button.')
