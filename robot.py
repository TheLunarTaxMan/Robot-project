from sbot import *

def Main():

def GetDistance():
  distance = arduino.measure_ultrasound_distance(,)

def rotateLeft():
  motors.set_power(0, 0.8)
  sleep(1)
  motors.set_power(0,0)
  
def rotateRight():
  motors.set_power(1, 0.8)
  sleep(1)
  motors.set_power(1,0)

def WriteStatusToLog():
  #put some stuff here
