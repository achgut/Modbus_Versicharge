#Imports
import time
from datetime import datetime
from struct import *
import Wallbox_read_Static
import Wallbox_read_Actual

Wallbox_read_Static.main()

try:
  
  while True :
    Wallbox_read_Actual.main()
 
    time.sleep(2)


except KeyboardInterrupt:
  print('Hello user you have pressed ctrl-c button.')

