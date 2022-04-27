#Testcv9: Figuring out how to turn buggy: useful
import RPi.GPIO as GPIO
import sys
from time import sleep
import time
import pigpio

fwdadjust = 0
bckadjust = 0
turnspd = 30
rtTime = 1.4
ltTime = 1.28
ltTimeAdj = 0.0
rtTimeAdj = 0.0

#servo constants



class MotorControl:


    def __init__(self, en, p1, p2):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.speed = 99
        self.dir = 1
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
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self.motorPin1,GPIO.HIGH)
        GPIO.output(self.motorPin2,GPIO.LOW)
#        if(speed != self.speed):
        self.speed = speed
        self.pw.ChangeDutyCycle(speed)
        print ("dtcy: ",speed)
        self.dir=1   #forward
        print("f", speed)

    def bck(self, speed):
        GPIO.setmode(GPIO.BCM)

        GPIO.output(self.motorPin2,GPIO.HIGH)
        GPIO.output(self.motorPin1,GPIO.LOW)
#         if(speed != self.speed):
        self.speed = speed
        self.pw.ChangeDutyCycle(speed)
        self.dir=0   #back
        print("bspd: ",self.speed)
        
    def adj(self, deg):
        self.speed += deg
        self.bck(self.speed)
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
        self.stop(self)
        GPIO.cleanup()

#Try to make buggy turn circle
#TestAll.py: Tests motors, serv, ultrasound
class CircleTest:
#    global speedleft,speed right
    speedleft = 30;
    speedright = 30;
    def __init__(self, en1, pin1, pin2, en2, pin3,pin4):
        GPIO.setmode(GPIO.BCM)
        self.ml = MotorControl(en1, pin1, pin2)
        self.mr = MotorControl(en2, pin3, pin4)
        
    def motorsSpeed(self, left, right):
        self.speedleft = left
        self.speedright = right
        
    def go(self):
        GPIO.setmode(GPIO.BCM)
        self.ml.bck(self.speedleft)
        self.mr.bck(self.speedright)
    
    def adjLeft(self,delta):
        self.delta = delta
        self.ml.adj(self.delta)
        print("l ",self.delta)
        
    def adjRight(self,delta):
        self.delta = delta
        self.mr.adj(self.delta)
        print("r ",self.delta)
        
    def stop(self):
        GPIO.setmode(GPIO.BCM)
        self.ml.stop()
        self.mr.stop()

    def quit(self):
        GPIO.setmode(GPIO.BCM)
        self.stop()
        GPIO.cleanup()

car = CircleTest(18,7,8,19,9,10)
car.motorsSpeed(30,30)
sl = 30
sr = 30
dleft = 2
dright = 2
while True:
    try:
        w = input()
        x=w[0]
        if x == "q":
            car.stop()
            car.quit()
            sys.exit()
        elif w[0:2] == "bl":#begin speed left
            sl = int(w[2:])            
        elif w[0:2] == "br":#begin speed right
            sr = int(w[2:])
        elif w[0:2] == "dl":#val to inc or dec speed
            dleft = int(w[2:])            
        elif w[0:2] == "dr":#val to inc or dec speed
            dright = int(w[2:])

        elif x == "l":
            car.adjLeft(dleft)
        elif x == "r":
            car.adjRight(dright)
        elif x == "k":#key to left of l
            nleft = -dleft
            car.adjLeft(nleft)
        elif x == "e":#key to left of r
            car.adjRight(-dright)
        elif x == "g":
            car.motorsSpeed(sl, sr)
            car.go()
        elif x == "s":
            car.stop()
        elif x == "p":
            print("sl: ", sl," sr: ", sr,
                  " dl: ",dleft," dr: ",dright) 
        else:
            print("doofus")
    except:
        ex = sys.exc_info()[0]
        print("Exception: ",ex)
        if(str(ex).find("Index") != -1):
            continue
        if(str(ex).find("Value") != -1):
            continue
                  
        print("Stopped by  user")
        break
        
            
                  
        
    
        
        
        


