#CarOnewheel
from MotorControl import MotorControl as Motor
import RPi.GPIO as GPIO
import pigpio
import time
import sys
leftEncPin = 27
rightEncPin = 22
whlLeft = Motor(7, 8, 18, leftEncPin)
whlRight = Motor(10, 9, 19, rightEncPin)
wheel = whlLeft
warmupTime = 400
power = 50
def getTimeInMillis():
    return (int)(time.time()*1000.0)
def bothcallback(channel):#akward due to python- self
    if(channel == leftEncPin):
        whlLeft.whlcallback()
    elif(channel == rightEncPin):
        whlRight.whlcallback()
pin = wheel.encPin
while True:
    print("l or r or g or q?")#Which wheel?
    k = input()
    if(k == 'q'):
        wheel.stop
        wheel.quit()
        sys.exit()
    elif(k == 'l'):
        wheel = whlLeft
    elif(k == 'r'):
        wheel = whlRight
    elif(k == 'g'):
        timeStart = getTimeInMillis() 
        break
missionTime = 4000
timeNow = timeStart
lastTime = timeNow
state = 0
lastState = 0
wheel.fwd(power)
dtList = list()
cnt = 0
while (getTimeInMillis() - timeStart)< missionTime:
    #how to read state of a GPIO input
    #state = input(wheel.encPin)
    #time.sleep(0.5)
    #if (state == 1):
        #state = 0
    #else:
    #    state = 1
    #print(state, lastState)
    GPIO.wait_for_edge(pin, GPIO.BOTH)
        
    lastState = state
    cnt = cnt + 1
    timeNow = getTimeInMillis()
    delT = timeNow - lastTime
    reading = input(pin)
    dtList.append((delT, reading))
    lastTime = timeNow
    #sleep(0.002)#bounce time?

wheel.stop()
print(cnt)
print(dtList)
wheel.quit()

        
    
    
    
    

    
    


