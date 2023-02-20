#CarBasic
#Controls car movement
import numpy as np
import RPi.GPIO as GPIO
from MotorControl import MotorControl

class CarBasic():
#a static table used by the correct function
    global corTable
    
#       5:0,20:1,50:2,100:3,150:4,320:101}
    
    def __init__(self, en1, pin1, pin2, en2, pin3,pin4):
        GPIO.setmode(GPIO.BCM)
        self.ml = MotorControl(en1, pin1, pin2, 'L')
        self.mr = MotorControl(en2, pin3, pin4, 'R')
        self.oldret = 0
        self.startLR = (0 ,0)

    def motorsSpeed(self, left, right):
        self.speedleft = left
        self.speedright = right
        
    def goBck(self):
        GPIO.setmode(GPIO.BCM)
        #back cause cam points rear
        self.ml.bck(self.speedleft)
        self.mr.bck(self.speedright)
    
    def goFwd(self):
        GPIO.setmode(GPIO.BCM)
        self.ml.fwd(self.speedleft)
        self.mr.fwd(self.speedright)
        
    def fwdRbck(self):
        GPIO.setmode(GPIO.BCM)
        print(self.speedleft, self.speedright)
        self.ml.fwdRbck(self.speedleft)
        self.mr.fwdRbck(self.speedright)
        
    
    def adjLeft(self,delta):
        self.delta = delta
        self.ml.adj(self.delta)
        print("l ",self.delta)
        
    def adjRight(self,delta):
        self.delta = delta
        self.mr.adj(self.delta)
        print("r ",self.delta)
    
    def curSpeed(self):
        return self.ml.curSpeed(), self.mr.curSpeed()
        
    def stop(self):
        GPIO.setmode(GPIO.BCM)
        self.ml.stop()
        self.mr.stop()

    def quit(self):
        GPIO.setmode(GPIO.BCM)
        self.stop()
        GPIO.cleanup()
    
    #Returns the correcton value based on the offset
    #This may change a lot based on experience
    corTable = np.array([[5,0],[20,1],
                         [30,2],[40,3],
                         [50,4],[80,5],
                         [300,5],[301,101]],np.int32)
    def setStartX(self, left, right):
        self.startLR = (left, right)
        
    def getStartX():
        return self.StartLR
    
    def correct(self, offset):
        sign = 1
        absOff = abs(offset)
        if absOff > offset:
            sign = -1
        ret = 101
        for i in range(len(corTable)):
            if (absOff <= corTable[i,0]):
                ret = sign * corTable[i,1]
                break
        if self.oldret == ret:
            return 0
        else:
            self.oldret = ret
        
        return ret

