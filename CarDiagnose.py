#CarDiagnose
from MotorControl1 import MotorControl1 as Motor
import RPi.GPIO as GPIO
import pigpio
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
fig,ax = plt.subplots()

GPIO.setmode(GPIO.BCM)
def getTimeInMillis():
    return (int)(time.time()*1000.0)

def cmToTicks(cm):
    return cm * 0.87

def degToTicks(deg):
    return deg * 0.23

leftPower = 0#start power left wheel
rightPower = 100
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
whlLeft.fwd(0)
whlRight.fwd(rightPower)
lastL = 0
lastR = 0
start = getTimeInMillis()
sumSeconds = seconds = 0
done = False
cntsL = list()
cntsR = list()
xs = list()
idx = 0
sumL = sumR = 0
currentR = currentL = 0
try:
    while (not done):
        currentL = whlLeft.getTicks()
        currentR = whlRight.getTicks()
        deltaL = currentL - lastL
        deltaR = currentR - lastR
        sumL = deltaL + sumL
        sumR = deltaR + sumR
#        print("Tk ",currentL,deltaL,\
#               currentR,deltaR)
        lastL = currentL
        lastR = currentR
        time.sleep(1)
        seconds += 1
        if seconds == 5:
            sumSeconds += 5
            seconds = 0
            leftPower = 5
            rightPower -= 5
            whlLeft.fwd(0)
            whlRight.fwd(rightPower)
            if(leftPower < 5 or\
               rightPower < 5):
                done = True
            print (sumSeconds, leftPower, rightPower, sumR)
            cntsL.append(deltaL)
            cntsR.append(deltaR)
            xs.append(sumSeconds)
    whlLeft.stop()
    whlRight.stop()
    print("done")
    dcntsL = np.array(cntsL)
    dcntsR = np.array(cntsR)
    dsecs = np.array(xs)
    print("^c terminates")
    ax.plot(dsecs,dcntsR)
    plt.show()
    sys.exit()
except KeyboardInterrupt:
    whlLeft.stop()
    whlRight.stop()
    time.sleep(0.5)
    print("Stopped by user")
    sys.exit()

    