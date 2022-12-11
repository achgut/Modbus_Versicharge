# Test Umschalten auf 1 Phasig beim Laden
# Auto angeschlossen, Läd 3phasig mit 15A, dann Start
# Max Current wird immer wieder verändert

#Imports
import time
from datetime import datetime
from struct import *
import Wallbox_MaxCurrent
import Wallbox_Pause
import Wallbox_Phasen

Warten = 120 # in Sekunden
try:
  
  print("Start Sequenz in ", str(Warten), "s")
  print(" ")
  time.sleep(Warten)
  
  print(datetime.now())
  Wallbox_MaxCurrent.main(10)
  print("Maxcurrent auf 10A")
  print(" ")
  time.sleep(Warten)

  print(datetime.now())
  Wallbox_MaxCurrent.main(15)
  print("Maxcurrent auf 15A")
  print(" ")
  time.sleep(Warten)

  print(datetime.now())
  Wallbox_MaxCurrent.main(7)
  print("Maxcurrent auf 7A")
  print(" ")
  time.sleep(Warten)

  print(datetime.now())
  Wallbox_Phasen.main()
  print("Umschalten auf 1phasig")
  print(" ")
  time.sleep(Warten)

  print(datetime.now())
  Wallbox_MaxCurrent.main(10)
  print("Maxcurrent auf 10A")
  print(" ")
  time.sleep(Warten)

  print(datetime.now())
  Wallbox_MaxCurrent.main(7)
  print("Maxcurrent auf 7A")
  print(" ")
  time.sleep(Warten)


except KeyboardInterrupt:
  print('Hello user you have pressed ctrl-c button.')

