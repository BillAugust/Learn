#SimpleLight - ttests lighting up an led
import RPi.GPIO as GPIO
import sys
from time import sleep
import time

light = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(light,GPIO.OUT)
while True:
    try:
        GPIO.output(light, True)
        condition = True
        while True:
            
            sleep(1)
            condition = not condition
            GPIO.output(light, condition)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)
        
        




