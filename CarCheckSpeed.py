#check car response
import RPi.GPIO as GPIO
import pigpio
import time
import keyboard as kbd
from MotorControl import MotorControl
from CarBasic import CarBasic
import sys
startLeft = 0
startRight = 30
inc = 5
maxSpeed = startLeft + startRight + inc#for reduc low or inc high 
speedLeft = startLeft
speedRight = startRight
car = CarBasic(18,7,8,19,9,10)
car.stop()
dir = 'f'
def getTimeInMillis():
    return (int)(time.time()*1000.0)

def missionTime():
    return getTimeInMillis() - missionStart
def incOrDec(high, low):
    # this is to keep the speed from going nuts
    print(high, low)
    rt = 1
    if(high + low + inc> maxSpeed):
        rt = -1
    return rt


timeList = list()
missionStart = getTimeInMillis()
timeList.append((speedLeft, speedRight,
                   missionStart - getTimeInMillis()))
tIdx = 1
#ki = ""
#while True:
    #ki = kbd.read_key()
    #if(ki != ""):
    #    print(ki)
    #    ki = ""
    
while True:
    car.motorsSpeed(speedLeft ,speedRight)
    
    uin = input()
    lft = speedLeft
    rt = speedRight
    if uin.startswith('q'):
        car.stop()
        car.quit()
        sys.exit()
    elif uin.startswith('s') or uin.startswith('S'):
        car.stop()
    elif uin.startswith('f'):
        car.goFwd()
        dir = 'f'
        timeList.append((startLeft,
                            startRight,
                            missionTime()))
        tIdx = tIdx+1
        
    elif uin.startswith('b'):
        car.goBck()
        dir = 'b'
    elif uin.startswith('l'):
        l = uin.split('l')
        sign = 1
        if l[1].startswith('-'):
            sign = -1
            l = l[1].split('-')
        if l[1].isnumeric():
            speedLeft = sign * int(l[1])
            car.motorsSpeed(speedLeft, speedRight)
#            car.goFwd()
        else:
            print("?")
    elif uin.startswith('r'):
        r = uin.split('r')
        sign = 1
        if r[1].startswith('-'):
            sign = -1
            r = r[1].split('-')
            
        if r[1].isnumeric():
            speedRight = sign * int(r[1])
            car.motorsSpeed(speedLeft, speedRight)
#            car.goFwd()
        else:
            print("?")
    elif uin.startswith('z'):
        adj = inc * incOrDec(speedLeft, speedRight)
        if(adj > 0):
            car.adjRight(adj)
        else:
            car.adjLeft(adj)
        (speedLeft, speedRight) = car.curSpeed()
        
    elif uin.startswith('x'):
        adj = inc * incOrDec(speedLeft, speedRight)
        if(adj > 0):
            car.adjLeft(adj)
        else:
            car.adjRight(adj)
        (speedLeft, speedRight) = car.curSpeed()
        
    elif uin.startswith('d') or uin.startswith('D'):
        #do over
        car.stop()
        speedLeft = startLeft
        speedRight = startRight
    elif uin.startswith('t'):
        (l,r,strt) = timeList[0]
        timeList[tIdx] = (startRight,
                           startLeft,
                           missionTime())
        tIdx = tIdx+1
        lft=0
        rt=0
    elif uin.startswith('a'):
        #go in circles Right or Left
        #if lft = 0 circle rt else rt =0 so circle left
        car.motorsSpeed(speedLeft, speedRight)

        nTimes = 50
        startUp = missionTime()
        tIdx = 0
        car.fwdRbck()
        while tIdx < nTimes: 
            time.sleep(0.1)
            timeList.append((lft, rt,
                              missionTime() - startUp))
            tIdx = tIdx+1
        car.stop()
        for i in range(len(timeList)):
            print(timeList[i])
    else:
        print("??")
#some saved code in case I want to revert
#after elif uin.startswith('z'):
#        l = uin.split('z')
#        s = +1
#        if l[1].startswith('-'):
#            s = -1
#            l = uin.split('-')
        
#        if l[1].isnumeric():
#            car.adjLeft(s * int(l[1]))
#        else:
#            print("?")
#            car.adjLeft(-1)
# after elif uin.startswith('x'):
#        r = uin.split('x')
#        s = +1
#        if r[1].startswith('-'):
#            s = -1
#            r = uin.split('-')
        
#        if r[1].isnumeric():
#            car.adjRight(s * int(r[1]))
#        else:
#            print("?")

        
        
    
        

    

