#MotorControl
#Controls one mmotor
import RPi.GPIO as GPIO
import sys
from time import sleep
import time
import pigpio

class MotorControl:


    def __init__(self, en, p1, p2):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.speed = 0
        self.dir = 1#fwd
        self.enPin = en
        self.motorPin1 = p1
        self.motorPin2 = p2
        GPIO.setup(p1,GPIO.OUT)
        GPIO.setup(p2,GPIO.OUT)
        GPIO.setup(en,GPIO.OUT)
        GPIO.output(p1,GPIO.LOW)
        GPIO.output(p2,GPIO.LOW)
        self.pw=GPIO.PWM(en,1000)
        self.pw.start(self.speed)
        

    def fwd(self, speed):
        if(abs(speed) > 100.0):
            speed =100.0
        if(speed < 0.0):
            speed = -speed
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self.motorPin1,GPIO.HIGH)
        GPIO.output(self.motorPin2,GPIO.LOW)
        if(speed != self.speed):
            self.speed = speed
            self.pw.ChangeDutyCycle(speed)
        self.dir=1   #forward
        print("f", speed)

    def bck(self, speed):
        if(abs(speed) > 100.0):
            speed =100.0
        if(speed < 0.0):
            speed = -speed
        GPIO.setmode(GPIO.BCM)
        print("backward")
        GPIO.output(self.motorPin2,GPIO.HIGH)
        GPIO.output(self.motorPin1,GPIO.LOW)
        if(speed != self.speed):
            self.speed = speed
            self.pw.ChangeDutyCycle(speed)
        self.dir=0   #back
        
    def adj(self, deg):
        self.speed += deg
        self.fwd(self.speed)
        print("spd ", self.speed, " deg ", deg)
                        
    def stop(self):
        GPIO.setmode(GPIO.BCM)
        print("stop")
        GPIO.output(self.motorPin1,GPIO.LOW)
        GPIO.output(self.motorPin2,GPIO.LOW)
        self.speed = 0
        self.dir=1   #forward

    def quit(self):
        GPIO.setmode(GPIO.BCM)
        self.stop()
