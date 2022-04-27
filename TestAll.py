#TestAll.py: Tests motors, serv, ultrasound
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
        self.speed = 25
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
        if(speed != self.speed):
            self.speed = speed
            self.pw.ChangeDutyCycle(speed)
        self.dir=1   #forward
        print("f", speed)

    def bck(self, speed):
        GPIO.setmode(GPIO.BCM)
        print("backward")
        GPIO.output(self.motorPin2,GPIO.HIGH)
        GPIO.output(self.motorPin1,GPIO.LOW)
        if(speed != self.speed):
            self.speed = speed
            self.pw.ChangeDutyCycle(speed)
        self.dir=0   #back
        
    def adj(self, deg):
        self.speed += deg
        self.fwd(self.speed)
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

class CarControl:
    #PID constants
    Ki = 0
    Kp = 1
    dt = 0.1
    #PID global
    iSum = 0 #actually PID should be a class -- later
    def __init__(self, en1, pin1, pin2, en2, pin3,pin4, servopin, echopin, triggerpin):
        GPIO.setmode(GPIO.BCM)
        self.ml = MotorControl(en1, pin1, pin2)
        self.mr = MotorControl(en2, pin3, pin4)
        self.servo = GPIO.setup(servopin, GPIO.OUT)
        self.trigger = GPIO.setup(triggerpin, GPIO.OUT)
        self.triggerpin = triggerpin
        self.echo = GPIO.setup(echopin, GPIO.IN)
        self.echopin = echopin
        self.servopin = servopin
        self.servo = pigpio.pi()
        self.servo.set_mode(servopin, pigpio.OUTPUT)
        self.servo.set_PWM_frequency( servopin, 50 )
        self.oldret = 0

    #PID helper fundtion without the D
    def PIinit(self, ki, kp, isum, dtime):
        global Ki, Kp, iSum, dt
        Ki = ki
        Kp = kp
        iSum = isum
        dt = dtime

    def PI(self, delta):
        global  iSum
        iSum += delta * dt
        ut = Kp*delta + Ki * iSum
        print(delta, " ", ut)
        return ut
    
    def fwd(self, speed):
        GPIO.setmode(GPIO.BCM)
        self.ml.fwd(speed)
        self.mr.fwd(speed + fwdadjust)

    def bck(self, speed):
        GPIO.setmode(GPIO.BCM)
        self.ml.bck(speed)
        self.mr.bck(speed + bckadjust)
        
    def adjust(self, ang):#ang in degrees
        self.ml.adj( -ang)

    def rturn(self):
        GPIO.setmode(GPIO.BCM)
        self.ml.fwd(turnspd)
        self.mr.fwd(1)
        sleep(rtTime) #time to go 90 deg
        self.ml.stop()
        self.mr.stop()

    def lturn(self):
        GPIO.setmode(GPIO.BCM)
        self.mr.fwd(turnspd)
        self.ml.fwd(1)
        sleep(ltTime) #time to go 90 deg
        self.mr.stop()
        self.ml.stop()

    def angleturn(self, angle):        #angle is 0 straightcw pos ccw neg
        #this angleturn may need work
        self.angle = int(angle)
        if (self.angle >= 0):
            turnTime = self.angle/90.0 * rtTime + rtTimeAdj
            self.ml.fwd(turnspd)
            self.mr.bck(0)
            sleep(turnTime)
            self.ml.stop()
            self.mr.stop()
        else:
            turnTime = abs(angle/90.0 * ltTime + ltTimeAdj)
            self.ml.bck(turnspd)
            self.mr.fwd(0)
            sleep(turnTime)
            self.ml.stop()
            self.mr.stop()
    def stop(self):
        GPIO.setmode(GPIO.BCM)
        self.ml.stop()
        self.mr.stop()
    def quit(self):
        GPIO.setmode(GPIO.BCM)
        self.stop()
        GPIO.cleanup()

    def setServo(self,degree):
        pw = (500 + 1000 * degree/90)
        self.servo.set_servo_pulsewidth(self.servopin, pw)
        
    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.triggerpin, GPIO.HIGH)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.triggerpin, GPIO.LOW)
     
        StartTime = time.time()
        StopTime = time.time()
     
        while GPIO.input(self.echopin) == 0:
            StartTime = time.time()
     
        while GPIO.input(self.echopin) == 1:
            StopTime = time.time()
     
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
     
        return distance

    

GPIO.setmode(GPIO.BCM)
car = CarControl(18,7,8,19,9,10,21,20,16)
#en1, motPin1, motoPin2, en2, motoPin3, motoPin4,
#servoPin, echo, trigger

while True:
    try:
        x = input()
        if x == "q":
            car.quit()
            GPIO.cleanup()
            sys.exit(0)
        elif x == "mot":
            car.fwd(30)
            sleep(2.0)
            car.stop()
            sleep(0.5)
            car.bck(30)
            sleep(2)
            car.stop()
            sleep(0.5)
            car.lturn()
            sleep(0.5)
            car.rturn()
            sleep(0.5)
            print("5 seconds to adjust")
            sleep(5.0)
            car.lturn()
            sleep(0.5)
            car.rturn()
            sleep(0.5)
            car.stop();
        elif(x == "srv"):
            car.setServo(0)
            sleep(2)
            car.setServo(180)
            sleep(2)
            car.setServo(90)
            car.stop()
        elif(x == "usnd"):
            car.stop()
            sleep(1)
            dist = car.distance()
            print(dist)
            sleep(2)
            rpt = 10
            while(rpt > 0):
                dist = car.distance()
                print(dist)
                sleep(0.5)
                rpt = rpt -1
            print("change target")
            sleep(2)
            rpt = 10
            while(rpt > 0):
                dist = car.distance()
                print(dist)
                sleep(0.5)
                rpt = rpt -1
            car.stop()
        elif(x == "avoid"):
             car.fwd(30)
             tstart = time.time()
            
             while(car.distance() > 10):
                 print(car.distance)
                 sleep(0.1)
             car.stop()
             tstop = time.time()
             sleep(1)
             car.bck(30)
             sleep(tstop - tstart)
             car.stop()
             print("Started: ", tstart, "Ran: ", tstop - tstart)
        elif(x == "gst2"): #Go striaght
            car.setServo(180)
            sleep(2)
            spd = 30
            newSpeed = spd
            strSpeed = newSpeed
            car.fwd(spd)
            
            middist = car.distance()
            ldist = 0
            adjSpeed = 1.0
            bot = 1.0 #back on track angle
            distDif = 0.5
            pointed = True
            while True:
                dist = car.distance()
                tdist = middist - dist
                ddist = tdist - ldist #dif of tdist - last
                if(abs(tdist) > 20): break #wall gone
                if(abs(tdist) > distDif):
                    newSpeed = newSpeed - adjSpeed * tdist
                    pointed = False
                else:
                    #car is going straight see if on midline
                        #hold this speed for later
                    if(pointed != True):
                        strSpeed = newSpeed
                        if(abs(tdist) > distDif):
                        #if car  not at middist line
                            if(abs(tdist) >= distDif):
                                if(tdist > 0):
                                    newSpeed = strSpeed + bot
                            else:
                                newSpeed = strSpeed - bot
                        pointed = True
                    #if already pointed
                    else:
                        if(abs(tdist) < distDif):
                            newSpeed = strSpeed
                print("{0:6.3f} ,{1:6.3f} ,{2:6.3f} ,{3:6.3f}".
                      format(tdist, ldist, ddist, newSpeed))
                #print(tdist,' ', ldist,' ', ddist,' ', newSpeed)
                ldist = tdist
        elif(x=="gst"):
            #PID try
            car.setServo(180)
            car.PIinit(0.0, 1.0, 0.0, 0.1)
            sleep(2)
            spd = 30
            middist = car.distance() #set point for dist
            ldist = middist
            adjSpeed = 0.0
            strt = time.time()
            car.fwd(spd)
            sleep(0.2)
            while (time.time() - strt) < 5:
                ddist = car.distance() - middist
                if(abs(ddist) > 20): break
                spd = car.PI(ddist)
                car.adjust(spd)
                #print(ddist)
                sleep(dt)
            print("broke ", ddist)
            car.stop()
            

            print("mid = ",middist, " spd = ", spd)
        elif(x == "gst1"): #Go striaght
            car.setServo(0)
            sleep(2)
            car.fwd(30)
            middist = car.distance()
            ldist = 0
            adjDist = 10
            while True:
                dist = car.distance()
                tdist = middist - dist
                ldist = tdist - ldist
                
                if(abs(tdist) > 20): break
                else:
                    if(abs(tdist) >5):
                        if((abs(tdist - ldist)) > 10):
                            print("spur?")
                        
                        if(tdist > 0):
                            car.adjust(adjDist)
                        else:
                            car.adjust(- adjDist)
                        ldist = tdist
                    else: #if signs of t & l differ halve adjustment
                        signt = tdist > 0
                        signl = ldist > 0
                        if(signl != signt):
                            adjDist = adjDist/2
                            print(adjDist)
                        
                            
                            
                    #sleep(0.1)
                    sleep(1.0)#debug
            car.stop()
            print("mid = ",middist, " cur = ", dist)
        
            
        elif(x == "s"):
            car.stop()
            
        elif(x == "f"):
            car.fwd(50)
            
        elif(x == "b"):
            car.bck(25)
            
        elif(x == "l"):
            car.lturn()
            
        elif(x == "r"):
            car.rturn()
        elif(x.isnumeric()):
            print(int(x))
            car.angleturn(int(x))
        elif(x.find("-") != -1):
            print(int(x))
            car.angleturn(int(x))
        elif(x == "quit"):
            print("All Done")
            GPIO.cleanup()
            sys.exit(0)
             
        else: print("no such")
    except KeyboardInterrupt:
        print("Emergency quit")
        GPIO.cleanup()
        sys.exit(0)