from MotorControl import MotorControl as Motor
import RPi.GPIO as GPIO
import pigpio
import time
import sys
leftEncPin = 27
rightEncPin = 22
whlLeft = Motor(8, 7, 18, leftEncPin)
whlRight = Motor(10, 9, 19, rightEncPin)
warmupTime = 400
missionLength = 10000 #Total time of mission
def getTimeInMillis():
    return (int)(time.time()*1000.0)
def bothcallback(channel):#akward due to python- self
    if(channel == leftEncPin):
        whlLeft.whlcallback()
    elif(channel == rightEncPin):
        whlRight.whlcallback()
#now setup left or right
GPIO.setmode(GPIO.BCM)
GPIO.add_event_detect(whlLeft.getEncPin(),
                        GPIO.RISING,
                        callback=whlLeft.wheelcallback,
                        bouncetime=2)
GPIO.add_event_detect(whlRight.getEncPin(),
                        GPIO.RISING,
                        callback=whlRight.wheelcallback,
                        bouncetime=2)
whlLeft.stop()
whlRight.stop()
time.sleep(.5)
whlLeft.setMissionStart(getTimeInMillis())
whlRight.setMissionStart(getTimeInMillis())
leftPower = 50#start power left wheel
rightPower = 50
#start power right wheel
inc = 1.0
tooDif = 10#Time dif in millis between wheel delTs
delInc = .2

dtList = list()
powerMax = leftPower + rightPower
whlLeft.fwd(leftPower)
whlRight.fwd(rightPower)
missionTime = getTimeInMillis()
while(getTimeInMillis() - missionTime < warmupTime):
    pass#Let buggy get up to speed
loops = 0
missionTime = getTimeInMillis()
whlLeft.setMissionStart(missionTime)
whlRight.setMissionStart(missionTime)
whlLeft.setModCnt(10)
whlRight.setModCnt(10)
evenerP = 0
evenerM = 0
while (getTimeInMillis() - missionTime) < missionLength:
    loops += 1
    time.sleep(0.01)
    lDt = whlLeft.getDt()
    rDt = whlRight.getDt()
    dtList.append(("l", lDt,
                   " r", rDt))

    if(abs(lDt - rDt) > tooDif):
        tim = getTimeInMillis() - missionTime
        dtList.append(("L", lDt,
                      " R", rDt))
        rp = whlRight.getPower()
        lp = whlLeft.getPower()
        inc = (abs((lDt - rDt)*delInc))
               
        if(inc <= 0):
            inc = 0
        if(inc>10):
            inc = 10
        if rp +lp > powerMax:
            if lDt == rDt:
                evenerP = (evenerP + 1) % 2
                if(evenerP == 0):
                    whlLeft.setPower(lp - inc)
                else:
                    whlRight.setPower(rp - inc)
            elif lDt < rDt:
                whlLeft.setPower(lp - inc)
            elif rDt < lDt:
                whlRight.setPower(rp - inc)
                
        else:
            if lDt == rDt:
                evenerM = (evenerM + 1) % 2
                if(evenerM == 0):
                    whlLeft.setPower(lp + inc)
                else:
                    whlRight.setPower(rp + inc)
            elif lDt < rDt:
                whlRight.setPower(rp + inc)
            elif rDt < lDt:
                whlLeft.setPower(lp + inc)
        whlLeft.fwd(whlLeft.getPower())
        whlRight.fwd(whlRight.getPower())
        dtList.append((tim, whlLeft.getPower(),
                        whlRight.getPower()))
                
  
whlLeft.stop()
whlRight.stop()
print(loops)
print("L",len(whlLeft.speedList),
      "R",len(whlRight.speedList))

print ("Left Speed  List")
print(whlLeft.speedList)
print ("Right Speed  List")
print(whlRight.speedList)
print(dtList)
whlRight.quit()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               