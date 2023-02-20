#attempt to figure out back/forward
import RPi.GPIO as GPIO
import sys
from time import sleep
import time
import pigpio
# 18,7,8,
en = 18
motorPin1 = 7
motorPin2 = 8
speed = 40

GPIO.setmode(GPIO.BCM)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(motorPin1,GPIO.OUT)
GPIO.setup(motorPin2,GPIO.OUT)
GPIO.output(motorPin1,GPIO.LOW)
GPIO.output(motorPin2,GPIO.HIGH)
pw=GPIO.PWM(en,1000)
pw.start(0)
pw.ChangeDutyCycle(speed)
print ("dcy = ", speed)
dir=1#forward
time.sleep(5)
GPIO.output(motorPin1,GPIO.LOW)
GPIO.output(motorPin2,GPIO.LOW)
time.sleep(1)
GPIO.output(motorPin1,GPIO.HIGH)
GPIO.output(motorPin2,GPIO.LOW)
pw.ChangeDutyCycle(speed)
print ("dcy = ", speed)
dir=1#forward
time.sleep(5)
GPIO.output(motorPin1,GPIO.LOW)
GPIO.output(motorPin2,GPIO.LOW)
time.sleep(1)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
sys.exit()

