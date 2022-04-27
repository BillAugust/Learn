#Speed Detect


#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import time, math, sys

import MotorControl
moto = MotorControl.MotorControl(18,9,10)

class SpeedMeas:
    def __init__(self, count, duration):
        self.count = count
        self.duration = duration
        
    
dist_meas = 0.00
km_per_hour = 0
rpm = 0
elapse = 0
sensor = 17
r_cm = 6.7 / 2#radius of wheel in cm
circ_cm = (2*math.pi)*r_cm  # calculate wheel circumference in CM
dist_km = circ_cm/100000    # convert cm to km
pulse = 0
start_timer = time.time()
global speedParams, needrecord
speedParams = list()
needrecord = False

def init_GPIO():					# initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def calculate_elapse(channel):# callback function
    global pulse, start_timer, elapse, speedParams
    global needrecord, new
    if needrecord:
        speedParams.append(SpeedMeas(9999, new))
        needrecord = False
    #print ("Hit ", len(speedParams))
    pulse+=1# increase pulse by 1 whenever interrupt occurred
    elapse = time.time() - start_timer# elapse for every 1 complete rotation made!
    newMeas = SpeedMeas(pulse, elapse)
    speedParams.append(newMeas)
    start_timer = time.time()# current time equals start_timer

def calculate_speed(elapse):
    global rpm,dist_km
    if elapse !=0:  # to avoid DivisionByZero error
        rpm = 60/elapse
        km_per_sec = dist_km / elapse   # calculate KM/sec
        km_per_hour = km_per_sec * 3600 # calculate KM/h
    else:
        km_per_hour = 0
    return km_per_hour

def init_interrupt():
    GPIO.add_event_detect(sensor, GPIO.RISING,
                          callback = calculate_elapse,
                          bouncetime = 200)

def atend():
    print ("atend called")    
    n = len(speedParams)
    tot = 0
    for i in range(n):
        print("Hit: ",speedParams[i].count,
              "Dur: ",speedParams[i].duration)
        tot += speedParams[i].duration
    print("____________")
    print("Total: ", tot," Avg: ",tot/n)


if __name__ == '__main__':
    init_GPIO()
    moto.fwd(40)
    init_interrupt()
    sleep(1)
    lastHit = -1
    needrecord = False
    new = 0
    while True:
        try:
            print("started wait loop")
            
            #this and calculate speed need serious work
            while(len(speedParams)<=0):
                pass#wait til an interrupt has occured
            print ("waitloop end")
               
            lastMeas = speedParams[-1]

#if(lastMeas.count != lastHit):
                #lastHit = lastMeas.count
                #kph = calculate_speed(lastMeas.duration)
                #kphp = int(kph*100)/100
                #print("hits: ",lastMeas.count,"KPH: ",kphp)
            userin = input()
            if userin.isnumeric():
                needrecord = True
                new = int(userin)
                moto.fwd(new)
            elif userin == "q":
                print("q hit")
                GPIO.cleanup()
                atend()
                sys.exit(0)
        except KeyboardInterrupt:
            print("Emergency quit")
            GPIO.cleanup()
            sys.exit(0)

