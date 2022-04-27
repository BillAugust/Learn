import RPi.GPIO as GPIO
from time import sleep

class MotorControl:
    dir=1   #forward
    speed=0    #low Speed

    def __init__(self, en, p1, p2):
        GPIO.setmode(GPIO.BCM)
        self.enPin = en
        self.motorPin1 = p1
        self.motorPin2 = p2
        GPIO.setwarnings(False)
        GPIO.setup(p1,GPIO.OUT)
        GPIO.setup(p2,GPIO.OUT)
        GPIO.setup(en,GPIO.OUT)
        GPIO.output(p1,GPIO.LOW)
        GPIO.output(p2,GPIO.LOW)
        self.pw=GPIO.PWM(en,1000)
        self.pw.start(self.speed)



    def fwd(self, speed):
        print("forward")
        GPIO.output(self.motorPin1,GPIO.HIGH)
        GPIO.output(self.motorPin2,GPIO.LOW)
        if(speed != self.speed):
            self.speed = speed
            self.pw.ChangeDutyCycle(speed)
        dir=1   #forward

    def bck(self, speed):
        print("backward")
        GPIO.output(self.motorPin1,GPIO.HIGH)
        GPIO.output(self.motorPin2,GPIO.LOW)
        if(speed != self.speed):
            self.speed = speed
            self.pw.ChangeDutyCycle(speed)
        dir=0   #back

    def stop(self):
        print("stop")
        GPIO.output(self.motorPin1,GPIO.LOW)
        GPIO.output(self.motorPin2,GPIO.LOW)
        self.speed = 0
        dir=1   #forward

    def quit(self):
        GPIO.cleanup()
        

print("Starting motor control")

mcl = MotorControl(18, 9, 10)
mcr = MotorControl(19, 7, 8)
while True:
    x = input("")
    if x=='f':
        mcl.fwd(50)
        mcr.fwd(50)
    elif x=='s':
        mcl.stop()
        mcr.stop()
    elif x=='q':
        mcl.quit()
        mcr.quit()
        GPIO.cleanup()

        break

    else:
        print ("doofus")


