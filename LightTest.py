#Light test
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

light = 17
button = 27
#GPIO.setup(button,GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(light,GPIO.OUT)

try:
    old_state = False
    while True:
        button_state = GPIO.input(button)
        print(button_state)
        if(button_state != old_state):
            GPIO.output(light, button_state)
            print("state changed")
            old_state = button_state
            
        time.sleep(0.2)
except:
    GPIO.cleanup()
