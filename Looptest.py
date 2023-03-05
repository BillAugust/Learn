from MotorControl import MotorControl as Motor
import RPi.GPIO as GPIO
import pigpio
import time
import sys

leftEncPin = 27
rightEncPin = 22
whlLeft = Motor(7, 8, 18, leftEncPin)
whlRight = Motor(10, 9, 19, rightEncPin)
leftPower = rightPower = 99
whlLeft.stop()
whlRight.stop()
whlLeft.fwd(leftPower)
whlRight.fwd(rightPower)
strt = int(time.time())
done = False
while done != True:
    time.sleep(0.1)
    now = int(time.time())
    if((now - strt) > 10):
        done = True;
whlLeft.stop()
whlRight.stop()
whlRight.quit()
sys.exit()

    