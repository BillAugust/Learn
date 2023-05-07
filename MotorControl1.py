#MotorControl
#Controls one mmotor
import RPi.GPIO as GPIO
import sys
from time import sleep
import time
import pigpio

class MotorControl1:
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
        self.targetDelT = 0
        self.delPower = 0
        self.targetDif = 0
        self.speedList = list()
        self.cal = False
        self.sumPower = 0.0
        self.modCnt = 1#can't be zero


    def setMissionStart(self, startTime):
        self.missionStart = startTime
        self.tenTime = self.missionStart

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
        self.modCnt = 10 #default.could be changed by setModCnt


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

    def curPower(self):
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
        return int(self.power)
    
    def getNumChanged(self):
        return self.numChange
    def getTicks(self):
        return self.numChange
        
    
    def getDt(self):
        return self.delT
    
    def setModCnt(self, cnt):
        self.modCnt = cnt
        
    def initWheelcallback(self,dp, tDT, tDf, cal):
        self.delPower = dp
        self.targetDelT = tDT
        self.targetDif = tDf
        self.cal = cal
        self.setModCnt(1)
        

    def wheelcallback(self, channel):
        self.numChange += 1
        self.sumPower += self.power
        #print(self.modCnt)

        if ((self.numChange % self.modCnt) == 0):
            delT = self.getTimeInMillis() - self.tenTime
            if(abs(delT) > 150):
                self.tenTime = self.getTimeInMillis()
                self.speedList.append((\
                    "***", self.numChange, delT))
                return
            self.tenTime = self.getTimeInMillis()
            dif = delT - self.targetDelT
            oldPower = self.power
            if(abs(dif) >= self.targetDif):
                self.power += dif * self.delPower
#                self.speedList.append((dif,\
#                                       self.power,\
#                                       self.delPower,\
#                                       oldPower))
                                       
                                       
                if(self.power > 100):
                    self.power = 100
                if(self.power <= 10):
                    self.power = 10
                if(not self.cal):
                    self.pw.ChangeDutyCycle(int(self.power))
            self.speedList.append((delT,
                                   int(self.power),
                                   oldPower,
                                   self.sumPower,
                                   self.numChange))
            
