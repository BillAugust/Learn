import RPi.GPIO as GPIO          
from time import sleep

#Be sure to change these
in1 = 8
in2 = 7
en = 9
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
r1=GPIO.PWM(in1,1000)
r2=GPIO.PWM(in2,1000)
p.start(25)
r1.start(25)
GPIO.output(in2,GPIO.LOW)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    
dutycyc = 25
needstart = True
while(1):

    x=input("")
   
    if x=='r':
        print("run")
        if(temp1==1):
         p.ChangeDutyCycle(dutycyc)
         r1.ChangeDutyCycle(dutycyc)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        p.ChangeDutyCycle(0)
        r1.ChangeDutyCycle(0)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        #GPIO.output(in2,GPIO.HIGH)
        if needstart:
           r2.start(dutycyc)
        else:
            r2.ChangeDutyCycle(dutycyc)
            needstart = False
            
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        dutycyc=25
        p.ChangeDutyCycle(dutycyc)
        r1.ChangeDutyCycle(dutycyc)
        x='z'

    elif x=='m':
        print("medium")
        dutycyc=50
        p.ChangeDutyCycle(dutycyc)
        r1.ChangeDutyCycle(dutycyc)
        x='z'

    elif x=='q':
        print("quick")
        dutycyc=75
        p.ChangeDutyCycle(dutycyc)
        r1.ChangeDutyCycle(dutycyc)
        x='z'

    elif x=='h':
        print("high")
        dutycyc=100
        p.ChangeDutyCycle(dutycyc)
        r1.ChangeDutyCycle(dutycyc)
        x='z'
     
   
    elif x=='e':
        GPIO.cleanup()
        break
   
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
