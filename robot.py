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

def whereami(): #finds the higest value id to go towards
    markerList = vision.detect_markers()
    if len(markerList) > 0:
        ID = markerList[0] 
        check = None
        for marker in markerList:
            if marker.id == 0 or marker.id == 1:
                check = marker.id
            val = marker.id
            if val > ID.id:
                ID = marker
        if check != None and (ID.id == 7 or ID.id == 6): #checks if 1 or 0 are seenin the edge case the robot sees them and 6
            return check
        return Id
    else:
        return None


def panick()
    #checks what current location is


#main starts here
arduino.set_pin_mode(AnalogPin.A5, GPIOPinMode.Input)
arduino.set_pin_mode(AnalogPin.A4, GPIOPinMode.Input)
arduino.set_pin_mode(AnalogPin.A3, GPIOPinMode.Input)
arduino.set_pin_mode(10, GPIOPinMode.Input)
arduino.set_pin_mode(11, GPIOPinMode.Input)
arduino.set_pin_mode(12, GPIOPinMode.Input)
arduino.set_pin_mode(13, GPIOPinMode.Input)


while True:
    UltraDistance = arduino.measure_ultrasound_distance(11,10)
    #Stores current QRCodes in List
    location = whereami()
    if location != None:
        if location.id == 0 or location.id == 1:
            markerchasing()
        elif location.id == 2 or location.id == 3 or location.id == 4 or location.id == 5:
            linefollowing()    
        elif location.id == 6 or location.id == 7:
            if location.location.distance > 500:
                markerchasing()
            else:
                #rotate about 90 degs left (doesnt need to be precise)
    else:
        panick()
 
    set_state(current_state)
