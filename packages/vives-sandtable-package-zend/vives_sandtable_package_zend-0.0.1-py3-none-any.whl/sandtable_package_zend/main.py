# zet hier de main klasse in als beginpunt van het programma

import numpy as np 
import serial 
from sender import Sender
from functions import Functions
import time


raspberry = Sender("ACM0")
testFunction = Functions()

#raspberry.send("G0 X10 Y10")

raspberry.initializeTable()
raspberry.manual_command()