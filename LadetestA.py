# Test Umschalten auf 1 Phasig
# Kein Auto angeschlossen
# Max Current wird immer wieder verändert
# Fehler 1: Max Current wird um 1A vermindert (10A -> 9A, 7A -> 6A)
# Fehler 2: Absturz nach einiger Zeit, nachdem auf 1phasig umgeschaltet und Max Current verändert wurde.


#Imports
import time
from datetime import datetime
from struct import *
import Wallbox_MaxCurrent
import Wallbox_Pause
import Wallbox_Phasen

Warten = 10 # in Sekunden
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

