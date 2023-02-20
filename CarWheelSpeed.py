#CarWheelSpeed
import RPi.GPIO as GPIO
import pigpio
import time
from MotorControl import MotorControl
import sys
def getTimeInMillis():
    return (int)(time.time()*1000.0)
missionStart = getTimeInMillis()
#The wheel speed callback is defined here
#WheelSpeed is a class to control a wheel with speed disc
class WheelSpeed:
    def __init__(self, en, p1, p2, encPin, totChange):
        self.wheel = MotorControl(
            self, en, p1, p2, encPin)
        self.lastTime = 0
        self.numChange = 0
        self.totChange = totChange
        self.encPin = encPin
    def wheelcallback(channel):
        global missionStart
        global leftEncPin
        global rightEncPin
        if(channel == leftEncPin):
            idx = 0
        elif(channel == rightEncPin):
            idx = 1
            
        t = getTimeInMillis() - missionStart
        if(lastTime[idx] == 0):
            tenTime[idx] = 0
            numChange[idx] = 0
        if ((numChange[idx] % 10) == 0):
            speedList.append(("---", channel,
                              t, t - tenTime[idx],
                              numChange[idx]))
            tenTime[idx] = t
        numChange += 1
        r = 0
        if(GPIO.input(channel) == True):
            r = 1
        if(numChange[idx]  > totChange):
            wheel.stop()
        lastTime = t
    
        
