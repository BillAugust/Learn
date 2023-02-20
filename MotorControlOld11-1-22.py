#MotorControl
#Controls one mmotor
import RPi.GPIO as GPIO
import sys
from time import sleep
import time
import pigpio

class MotorControl:
    newlftSpeed = 0
    speedList = list()
    def getTimeInMillis(self):
        return (int)(time.time()*1000.0)
    
    def __init__(self, p1, p2, en, encPin, id = 'N'):
        print(p1,p2,en,encPin)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.power = 0
        self.numChange = 0;
        self.dir = 1#fwd
        self.enPin = en
        self.encPin = encPin
        self.motorPin1 = p1
        self.motorPin2 = p2
        GPIO.setup(p1,GPIO.OUT)
        GPIO.setup(p2,GPIO.OUT)
        GPIO.setup(en,GPIO.OUT)
        GPIO.output(p1,GPIO.LOW)
        GPIO.output(p2,GPIO.LOW)
        GPIO.setup(encPin,GPIO.IN)
        self.pw=GPIO.PWM(en,1000)
        self.pw.start(self.power)
        
        self.id = id
        self.missionStart = (int)(time.time()*1000.0)
        self.tenTime = 0
        self.delT = 0

    def setMissionStart(self, startTime):
        self.missionStart = startTime 

    def getEncPin(self):
        return self.encPin
    
    def getID(self):
        return self.id

    def fwd(self, power, adjusting = False):
        if(abs(power) > 100.0):
            power =100.0
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self.motorPin1,GPIO.HIGH)
        GPIO.output(self.motorPin2,GPIO.LOW)
#        if(not adjusting): #this did not adjust > delta
# If want that, uncomment previous line and tab next
        self.power = power
        self.pw.ChangeDutyCycle(power)
        self.dir=1   #forward

    def bck(self, power, adjusting = False):
        if(abs(power) > 100.0):
            power =100.0
#        if(not adjusting): #see comment under fwd
        newSpeed = power
        GPIO.setmode(GPIO.BCM)
        print("backward: ", power)
        GPIO.output(self.motorPin2,GPIO.HIGH)
        GPIO.output(self.motorPin1,GPIO.LOW)
        
        self.power = power
        self.pw.ChangeDutyCycle(power)
        self.dir=0   #back
        
    def fwdRbck(self, power):#fwd if power pos else bck
        print('ID = ', self.id, power)
        if power < 0:
            self.bck(-power)
            print("is bck")
        else:
            self.fwd(power)
        
    def adj(self, deg):
        self.power = self.curSpeed() + deg
        if(self.dir == 0):
            self.bck(int(self.power), True)
        else:
            self.fwd(int(self.power), True)
        print("spd ", self.power, " deg ", deg)

    def curSpeed(self):
        return self.power
                       
    def stop(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self.motorPin1,GPIO.LOW)
        GPIO.output(self.motorPin2,GPIO.LOW)
        self.power = 0
        self.dir=1   #forward
        print(self.motorPin1,self.motorPin2,self.power)
        

    def quit(self):
        GPIO.setmode(GPIO.BCM)
        self.stop()
        GPIO.cleanup()
        time.sleep(0.5)
    
    def setPower(self,pow):#sets the power (0 t0 100)
        # the argument is the numberthat will be used
        #in the next call to fwd
        if(pow < 0):pow = 0
        if(pow > 100):pow = 100
        self.power = pow
        
        
    def getPower(self):
        return self.power
    
    def changed(self):
        return False
    
    def getDt(self):
        return self.delT

    def wheelcallback(self, channel):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.encPin, GPIO.IN)
        t = self.getTimeInMillis() - self.missionStart
        
        if ((self.numChange % 10) == 0):
            self.delT = t - self.tenTime
            self.speedList.append(("---", self.encPin,
                              t, self.delT,
                              self.numChange))
            self.tenTime = t
        self.numChange += 1
        r = 0
        if(GPIO.input(self.encPin) == True):
            r = 1
#        if(numChange  > totChange):
#           wheel.stop()
        lastTime = t
