from sbot import arduino, motors, utils, AnalogPin, vision, GPIOPinMode
import math


listOfMarkerDistances = []
# robot = Robot()
track67 = False


def set_motors(left, right):
    motors.set_power(0, left)
    motors.set_power(1, right)
    
def set_state(state, turnSpeed, forwardSpeed):
    if state == "forward":
        set_motors(0.2,0.2)
    elif state == "left":
        set_motors(forwardSpeed,turnSpeed)
    elif state == "right":
        set_motors(turnSpeed, forwardSpeed)
    elif state == "stop":
        set_motors(0,0)

#calculates marker distances
def markerLocater(markerList):
    closest = markerList[0]
    for marker in markerList:
        distance = marker.position.distance
        if distance > closest.position.distance:
            closest = marker
    return closest


def markerSpeed(state, turnSpeed, forwardSpeed):
    if state == "forward":
        set_motors(forwardSpeed,forwardSpeed)
    elif state == "left":
        set_motors(forwardSpeed,turnSpeed)
    elif state == "right":
        set_motors(turnSpeed, forwardSpeed)
    

def markerchasing(marker):
    forwardSpeed = 0.1
    turnSpeed = 0.15
    print("markerchasing")
    current_state = ""
    turnAngle = marker.position.horizontal_angle
    if turnAngle == turnAngletemp:
        current_state "left"
        turnSpeed = -1 * turnSpeed
        forwardSpeed = 0.2 * turnSpeed
    elif turnAngle < 0.2:
        print("turning right")
        current_state = "right"
    elif turnAngle > -0.2:
        print("turning left")
        current_state = "left"
    else:
        print("turning forward")
        current_state = "forward"
        forwardspeed = forwardspeed * 3
    if turnAngle > abs(0.6):
        print("drifty boyo")
        turnSpeed = turnSpeed * 1.15
        forwardSpeed = turnSpeed * -1
    elif turnAngle < abs(0.1):
        print("speedy boyo")
        forwardSpeed = turnSpeed * 2
        turnAngletemp = turnAngle
    set_state(current_state, turnSpeed, forwardSpeed)

def linefollowing():
    forwardSpeed = 0.1
    turnSpeed = 0.15
    current_state = ""
    left_IR = arduino.analog_read(AnalogPin.A0)
    centre_IR = arduino.analog_read(AnalogPin.A1)
    right_IR = arduino.analog_read(AnalogPin.A2)
    print(left_IR, centre_IR, right_IR)
    if left_IR < 1.2 and centre_IR > 3.5 and right_IR < 1.2:
        current_state = "forward"
    if left_IR < 1.2 and centre_IR > 1.2 and right_IR < 3.5:
        current_state = "left"
    if left_IR < 3.5 and centre_IR > 1.2 and right_IR < 1.2:
        current_state = "right"
    if left_IR < 3.5 and centre_IR < 3.5 and right_IR < 3.5:
        print("tokyo drift")
        turnSpeed = turnSpeed * 1.3
        forwardSpeed = turnSpeed * -1
        set_state(current_state, turnSpeed, forwardSpeed)
        
    set_state(current_state, turnSpeed, forwardSpeed)

def whereami(): #finds the higest value id to go towards
    
    markerList = vision.detect_markers()
    if len(markerList) > 0:
        ID = markerLocater(markerList)
        check = None
        for marker in markerList:
            if (marker.id == 6 or marker.id == 7) and marker.position.distance > 4000:
                print("saw em")
            else:
                if marker.id == 0 or marker.id == 1:
                    check = marker.id    
                val = marker.id
                if val > ID.id:
                    ID = marker
        if check != None and (ID.id == 7 or ID.id == 6): #checks if 1 or 0 are seen in the edge case the robot sees them and 6
            return check
        if (marker.id == 6 or marker.id == 7) and marker.position.distance > 4000:
            linefollowing()
        if (marker.id == 6 or marker.id == 7) and track67 == True:
            print("UltraViolet Code")
            markerchasing(marker)
        return ID
    else:
        return None


def panick():
    if track67 == True:
        set_state("left", 0.1, -0.1)
        location = whereami()
        if location == None:
            print("no markers yet")
        elif location.id == 6 or location.id == 7:
            print("ULTRASOUNDLOCK")
            set_state("stop", 0, 0)
            utils.sleep(2)
    else:
        frontDistance = arduino.measure_ultrasound_distance(2, 3)
        if frontDistance == 0:
            frontDistance = 4000
        #rightDistance = arduino.measure_ultrasound_distance(13, 12)
        if frontDistance < 50:
            print("reverse")
            set_motors(-0.3,-0.3)
        # elif rightDistance < 50:
             # print("turnleft")
             # set_motors(-0.3,-0.2)
            # #reverse turning left
        # elif leftDistance < 50:
            # print("turn right")
            # set_motors(-0.3,-0.2)
        if whereami() == None:
            set_state("left", -0.1, 0.1)
            utils.sleep(0.2)
        else:
            print("do a barrel roll")
            #do a 360 (4 seperate 90 deg turns) and follow highest value target
        #checks what current location is


#main starts here
arduino.set_pin_mode(AnalogPin.A2, GPIOPinMode.INPUT)
arduino.set_pin_mode(AnalogPin.A1, GPIOPinMode.INPUT)
arduino.set_pin_mode(AnalogPin.A0, GPIOPinMode.INPUT)
arduino.set_pin_mode(3, GPIOPinMode.INPUT)
arduino.set_pin_mode(2, GPIOPinMode.OUTPUT)
arduino.set_pin_mode(12, GPIOPinMode.INPUT)
arduino.set_pin_mode(13, GPIOPinMode.OUTPUT)


while True:
    UltraDistance = arduino.measure_ultrasound_distance(2,3)
    #Stores current QRCodes in List
    location = whereami()
    if track67 == False:
        if location != None:
            if location.id == 0 or location.id == 1:
                # markerchasing()
                print("YAY 1")
            elif location.id == 2 or location.id == 3 or location.id == 4 or location.id == 5:
                if location.id == 2 or location.id == 3 or ((location.id == 4 or location.id == 5) and location.position.distance > 1800):
                    linefollowed = linefollowing()
                else:
                    print("I'M GONNA STOP")
                    track67 = True
                    current_state = "stop"
                    set_state(current_state, 0, 0)
                    panick()
                        
            elif location.id == 6 or location.id == 7:
                print("I SEE 6 OR 7!")
                if location.position.distance < 4220:
                    # markerchasing()
                    print("YAY 2")
                else:
                    print("rotationneeded")
                    #rotate about 90 degs left (doesnt need to be precise)
        else:
            panick()
    else:
        print("targeting 67")
