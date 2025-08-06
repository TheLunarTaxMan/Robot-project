from sbot import arduino, motors, utils, AnalogPin, vision
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
    for marker in markerList:
        distance = marker.position.distance
        listOfMarkerDistances.append(distance)

while True:
    left_IR = arduino.analog_read(AnalogPin.A0)
    centre_IR = arduino.analog_read(AnalogPin.A1)
    right_IR = arduino.analog_read(AnalogPin.A2)
    UltraDistance = arduino.measure_ultrasound_distance(2,3)
    #Stores current QRCodes in List
    markerList = vision.detect_markers()
    if len(markerList) > 0:
        markerLocater(markerList)
        #Finds smallest value in List
        markerTargeted = min(listOfMarkerDistances)
        if markerTargeted >= 300 and markerTargeted <= 3000:
            #Find of a way to identify which marker corresponds to the shortest distance
            
            
            turnAngle = markerTargeted.position.horizontal_angle
        else:
            turnAngle = 0.3
        listOfMarkerDistances.clear()
        
    else:
        print("nomarkers")
    print(left_IR, centre_IR, right_IR)
    if left_IR < 1.2 and centre_IR > 3.5 and right_IR < 1.2:
        current_state = "forward"
    if left_IR < 1.2 and centre_IR > 1.2 and right_IR < 3.5:
        current_state = "left"
    if left_IR < 3.5 and centre_IR > 1.2 and right_IR < 1.2:
        current_state = "right"
    markerList.clear()
    set_state(current_state)