from sbot import arduino, motors, utils, AnalogPin, vision, GPIOPinMode
import math


listOfMarkerDistances = []
# robot = Robot()

def set_motors(left, right):
    motors.set_power(0, left)
    motors.set_power(1, right)
    
def set_state(state):
    if state == "forward":
        set_motors(0.2,0.2)
    elif state == "left":
        set_motors(0.2,turnAngle)
    elif state == "right":
        set_motors(turnAngle, 0.2)

#calculates marker distances
def markerLocater(markerList):
    closest = markerList[0]
    for marker in markerList:
        distance = marker.position.distance
        if distance > closest.position.distance:
            closest = marker
    return closest


def markerchasing():
    markerList = vision.detect_markers()
    if len(markerList) > 0:
        markerTargeted = markerLocater(markerList)
        #Finds smallest value in List
        if markerTargeted.location.distance >= 300 and markerTargeted.location.distance <= 3000:
            #Find of a way to identify which marker corresponds to the shortest distance
            turnAngle = markerTargeted.position.horizontal_angle
        else:
            turnAngle = 0.3 
        return True       
    else:
        print("nomarkers")
        return False

def linefollowing():
    left_IR = arduino.analog_read(AnalogPin.A3)
    centre_IR = arduino.analog_read(AnalogPin.A4)
    right_IR = arduino.analog_read(AnalogPin.A5)
    print(left_IR, centre_IR, right_IR)
    if left_IR < 1.2 and centre_IR > 3.5 and right_IR < 1.2:
        current_state = "forward"
    if left_IR < 1.2 and centre_IR > 1.2 and right_IR < 3.5:
        current_state = "left"
    if left_IR < 3.5 and centre_IR > 1.2 and right_IR < 1.2:
        current_state = "right"

def whereami():
    return 1

arduino.set_pin_mode(AnalogPin.A5, GPIOPinMode.Input)
arduino.set_pin_mode(AnalogPin.A4, GPIOPinMode.Input)
arduino.set_pin_mode(AnalogPin.A3, GPIOPinMode.Input)

arduino.set_pin_mode(10, GPIOPinMode.Input)
arduino.set_pin_mode(11, GPIOPinMode.Input)
arduino.set_pin_mode(12, GPIOPinMode.Input)
arduino.set_pin_mode(13, GPIOPinMode.Input)


chasing = False

while True:
    UltraDistance = arduino.measure_ultrasound_distance(11,10)
    #Stores current QRCodes in List
    location = whereami()
    if location == 1 or location == 2:
        chasing = True
    elif location == 3 or location == 4:
        chasing = False
    else:
        chasing = False
    
    

    if chasing:
        markerchasing()
    else:
        linefollowing()    
    set_state(current_state)