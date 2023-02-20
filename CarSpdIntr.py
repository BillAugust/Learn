#CarSpdIntrpt
import RPi.GPIO as GPIO
import pigpio
import time
import keyboard as kbd
from MotorControl import MotorControl
#from CarBasic import CarBasic
#import rotary_encoder
import sys
import signal
def getTimeInMillis():
    return (int)(time.time()*1000.0)
missionStart = getTimeInMillis()
def missionTime():
    return getTimeInMillis() - missionStart
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
GPIO.setmode(GPIO.BCM)    
wheelLeft = MotorControl(18,7,8,22)
wheelRight = MotorControl(19,10,9,27)
wheel = wheelLeft
global numChange
numChange = 0
lastTime = 0
cbInited = False
global wheelSpeed
global wheelStart
wheelStartLeft = 45
wheelStartRight = 75
global wheelInc
wheelInc = 5
global wheelTopSpeed
wheelTopSpeed = 100
wheelStart = wheelStartLeft
wheelSpeed = wheelStart
global incing #True if we are doing multiple speeds
incing = False 
global numPerSpeed
numPerSpeed = 500
speedList = list()

def wheelcallback(channel):
    global numChange
    global missionStart
    global wheelSpeed
    global wheelStart
    global wheelInc
    global wheelTopSpeed
    global incing
    global numPerSpeed
    global speedList
    global lastTime
    global numChange
    global tenTime
    
    t = getTimeInMillis() - missionStart
    if(lastTime == 0):
        tenTime = 0
    
        
    
    if ((numChange % 10) == 0):
        speedList.append(("---", channel, wheelSpeed,
                         t, t - tenTime,
                         numChange))
        tenTime = t
    numChange += 1
    r = 0
    if(GPIO.input(wheel.getEncPin()) == True):
        r = 1
    if ((numChange > 50)and incing):
        speedList.append((wheelSpeed,
                         t, t - lastTime,
                         numChange))
        wheelSpeed = wheelSpeed + wheelInc
        if wheelSpeed > wheelTopSpeed:
            wheel.stop()
            time.sleep(0.5)
        else:
            wheel.fwd(wheelSpeed)
            lastTime = t
            numChange = 0
            
    elif(numChange > 150):
        wheel.stop()
        lastTime = t
    lastTime = t
        
            

GPIO.setup(wheelLeft.getEncPin(),GPIO.IN)
GPIO.setup(wheelRight.getEncPin(),GPIO.IN)

timeList = list()
changeList = list()

while True:
    uin = input()
    if(uin.startswith('q')):
        wheelLeft.stop()
        wheelRight.stop()
        wheelLeft.quit()# this will do cleanup
        sys.exit(0)

    if(uin.startswith('s')):
        wheel.stop()
    
    if(uin.startswith('f')):
        wheel.fwd(70)
        timeList.clear()
        changeList.clear()
        missionStart = getTimeInMillis()
        numHits = 0
        numChange = 0
        l = 1
        while numHits<10000:
            r = 0
            if(GPIO.input(wheel.getEncPin()) == True):
                r = 1
            t = getTimeInMillis() - missionStart
            if (r != l):
                #changeList.append((t, r))
                l = r
                numChange += 1
            timeList.append((t, r))
            numHits += 1
            time.sleep(0.001)
        lastTime = t
        wheel.stop()
        print("Stop")

    if(uin.startswith('a')):
        for i in range(len(timeList)):
            print(timeList[i])
    if(uin.startswith('c')):
        print(numChange)
        #for i in range(len(changeList)):
            #print(changeList[i])
        print(numChange)
        rots = numChange/40.0
        print("Rotations: ", rots)
        rps = rots/(lastTime/1000.0)                               
        print("rps: ", rps, "lastTime: ", lastTime)
    if(uin.startswith('d')):
        for k in range(len(speedList)):
            print(speedList[k])
       
        
#interrupt handling init code
    if uin.startswith('i') or uin.startswith('j'):
        
        incing = uin.startswith('j') 
        numChange = 0
        if not cbInited:
            
            GPIO.add_event_detect(wheelLeft.getEncPin(),
                                  GPIO.BOTH,
                                  callback=wheelcallback,
                                  bouncetime=2)
            GPIO.add_event_detect(wheelRight.getEncPin(),
                                  GPIO.BOTH,
                                  callback=wheelcallback,
                                  bouncetime=2)
            cbInited = True
            
        wheel.fwd(wheelStart)
        wheelSpeed = wheelStart
        changeList.clear()
        speedList.clear()
        missionStart = getTimeInMillis()
        lastTime = 0
        
    if uin.startswith('l'):
        wheel = wheelLeft
        wheelStart = wheelStartLeft
        GPIO.setmode(GPIO.BCM)    

    if uin.startswith('r'):
        wheel = wheelRight
        wheelStart = wheelStartRight
        GPIO.setmode(GPIO.BCM)    
        
