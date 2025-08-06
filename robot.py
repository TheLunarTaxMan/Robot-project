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


def markerchasing(marker):
    print("markerchasing")
        #Finds smallest value in List
        if marker.position.distance >= 300 and markerTargeted.position.distance <= 3000:
            turnAngle = markerTargeted.position.horizontal_angle
            
        else:
            turnAngle = 0.3 
        return True       

def linefollowing():
    print("line following")
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
            if (marker.id == 6 or marker.id == 7) and marker.postion.distance < 2200:
                print("saw em")
            else:
                if marker.id == 0 or marker.id == 1:
                    check = marker.id    
                val = marker.id
                if val > ID.id:
                    ID = marker
        if check != None and (ID.id == 7 or ID.id == 6): #checks if 1 or 0 are seen in the edge case the robot sees them and 6
            return check
        return Id
    else:
        return None


def panick()
    print("PANICKING!!!")
    #checks what current location is
    leftDistance = arduino.measure_ultrasound_distance(11, 10)
    rightDistance = arduino.measure_ultrasound_distance(13, 12)
    if rightDistance < 50 and leftDistance < 50:
        #reverse 
    elif rightDistance < 50:
        #reverse turning left
    elif leftDistance < 50:
        #revers turing right
    else:
        #do a 360 (4 seperate 90 deg turns) and follow highest value target
        


#main starts here
arduino.set_pin_mode(AnalogPin.A5, GPIOPinMode.Input)
arduino.set_pin_mode(AnalogPin.A4, GPIOPinMode.Input)
arduino.set_pin_mode(AnalogPin.A3, GPIOPinMode.Input)
arduino.set_pin_mode(10, GPIOPinMode.Input)
arduino.set_pin_mode(11, GPIOPinMode.Output)
arduino.set_pin_mode(12, GPIOPinMode.Input)
arduino.set_pin_mode(13, GPIOPinMode.Output)


while True:
    UltraDistance = arduino.measure_ultrasound_distance(11,10)
    #Stores current QRCodes in List
    location = whereami()
    print("i am following ID " + str(location.id))
    if location != None:
        if location.id == 0 or location.id == 1:
            if arduino.analog_read(AnalogPin.A3) > 200 or arduino.analog_read(AnalogPin.A4) > 200 or arduino.analog_read(AnalogPin.A5) > 200:
                #stop and rotate 90 left 
            markerchasing(location)
        elif location.id == 2 or location.id == 3 or location.id == 4 or location.id == 5:
            linefollowing()    #we need a check for if we actually know where the line is
        elif location.id == 6 or location.id == 7:
            if location.position.distance > 500:
                markerchasing()
            else:
                #rotate about 90 degs left (doesnt need to be precise)
    else:
        panick()
 
    set_state(current_state)
