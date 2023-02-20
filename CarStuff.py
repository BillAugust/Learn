#CarStraight
#CarSpdIntrpt
import RPi.GPIO as GPIO
import pigpio
import time
import keyboard as kbd
from MotorControl import MotorControl
from CarWheelSpeed import WheelSpeed
import sys

def getTimeInMillis():
    return (int)(time.time()*1000.0)
missionStart = getTimeInMillis()
totChange = 300

wheelLeft = MotorControl(18,7,8,22, totChange)
wheelRight = MotorControl(19,9,10,27, totChange)
cbInited = False

#cwsl = CarWheelSpeed(wheelLeft.get


while True:
    uin = input()
    if(uin.startswith('q')):
        wheelLeft.stop()
        wheelRight.stop()
        wheelLeft.quit()# this will do cleanup
        sys.exit(0)

    if(uin.startswith('s')):
        wheelLeft.stop()
        wheelLeft.stop()

    if(uin.startswith('g')):
        if not cbInited:
            
            GPIO.add_event_detect(wheelLeft.getEncPin(),
                                  GPIO.BOTH,
                                  callback=wheelcallback,
                                  bouncetime=2)
            GPIO.add_event_detect(wheelRight.getEncPin(),
                                  GPIO.BOTH,
                                  callback=wheelcallback,
                                  bouncetime=2)
            cbInited = True
            
    

 