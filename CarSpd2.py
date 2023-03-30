from MotorControl1 import MotorControl1 as Motor
import RPi.GPIO as GPIO
import pigpio
import time
import sys
GPIO.setmode(GPIO.BCM)
def getTimeInMillis():
    return (int)(time.time()*1000.0)

def cmToTicks(cm):
    return cm * 0.87

def degToTicks(deg):
    return deg * 0.23

#print(cmToTicks(1500), degToTicks(90))
#sys.exit()

missionLength = 3800 #Total time of mission - not used
missionTicks = 90#number of ticks until stop

leftPower = 99#start power left wheel
rightPower = 0

leftEncPin = 22
rightEncPin = 27
whlLeft = Motor(7, 8, 18, leftEncPin)
whlRight = Motor(10, 9, 19, rightEncPin)
#now setup left and right
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
time.sleep(0.5)
whlLeft.setMissionStart(getTimeInMillis())
#start power right wheel
whlRight.setMissionStart(getTimeInMillis())

dtList = list() 
actionList = list()
#0 = done 1 = left. 2 = right, 3 = both
#0 = stop,1 = straight, 2 = lt turn, 3 = rt turn
#third parameter is dist in cm, or angle in degrees, 
#or time to stop in ms
actionList.append((3, 1, 150))
actionList.append((3, 0, 500))
actionList.append((3, 2, 360))
actionList.append((3, 0, 500))
actionList.append((3, 1, 150))
actionList.append((0, 0, 0))

#previus code goes 150 cm, stops, turns around, stops,
#goes back 150, then stops

whlLeft.fwd(10)
whlRight.fwd(10)
time.sleep(0.5)
whlLeft.fwd(leftPower)
whlRight.fwd(rightPower)
loops = 0
missionTime = getTimeInMillis()
whlLeft.setMissionStart(missionTime)
whlRight.setMissionStart(missionTime)
whlLeft.setModCnt(1)
whlRight.setModCnt(1)
cal = False
#array of actions to be preformed
whlLeft.initWheelcallback(0.5, 40, 3, cal)
#delta power, target dt, dif ignore if <= 3, do cal or not
whlRight.initWheelcallback(0.5, 40, 3, cal)
#while (getTimeInMillis() - missionTime < missionLength):
try:
    while (whlLeft.getNumChanged() < missionTicks) &\
          (whlRight.getNumChanged() < missionTicks):
        time.sleep(0.1)#all computation done in interrupt 
except KeyboardInterrupt:
    whlLeft.stop()
    whlRight.stop()
    time.sleep(0.5)
    print("Stopped by user")
    sys.exit()
    
    
whlLeft.stop()
whlRight.stop()

print(loops)
print("spdL",len(whlLeft.speedList),
      "spdR",len(whlRight.speedList))

print ("Left Speed  List")
print(whlLeft.speedList)
print ("Right Speed  List")
print(whlRight.speedList)
leftAvg = rightAvg = 0
print("L Change, Powersum",whlLeft.getNumChanged(),\
      whlLeft.sumPower)
print("R Change, Powersum",whlRight.getNumChanged(),\
      whlRight.sumPower)
if(whlLeft.numChange != 0):
    leftAvg = whlLeft.sumPower/whlLeft.numChange
if(whlRight.numChange != 0):
    rightAvg = whlRight.sumPower/whlRight.numChange
print("Lt Avg", leftAvg, "Rt Avg", rightAvg) 

whlRight.quit()
sys.exit()


