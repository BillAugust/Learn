#CarDiagnose
from MotorControl1 import MotorControl1 as Motor
import RPi.GPIO as GPIO
import pigpio
import time
import sys
GPIO.setmode(GPIO.BCM)
def getTimeInMillis():
    return (int)(time.time()*1000.0)

def cmToTicks(cm):
    return cm * 0.87

def degToTicks(deg):
    return deg * 0.23

leftPower = 99#start power left wheel
rightPower = 99
leftEncPin = 22
rightEncPin = 27
whlLeft = Motor(7, 8, 18, leftEncPin)
whlRight = Motor(9, 10, 19, rightEncPin)
#now setup left and right
GPIO.add_event_detect(whlLeft.getEncPin(),
                        GPIO.RISING,
                        callback=whlLeft.wheelcallback,
                        bouncetime=2)
GPIO.add_event_detect(whlRight.getEncPin(),
                        GPIO.RISING,
                        callback=whlRight.wheelcallback,
                        bouncetime=2)
whlLeft.stop()
whlRight.stop()
time.sleep(0.5)
whlLeft.fwd(60)
whlLeft.fwd(60)
try:
    while True:
        print("Tk ",whlLeft.getTicks(),\
              whlRight.getTicks())
        time.sleep(0.5)
except KeyboardInterrupt:
    whlLeft.stop()
    whlRight.stop()
    time.sleep(0.5)
    print("Stopped by user")
    sys.exit()

    