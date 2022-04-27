#SimpleSwitch
import RPi.GPIO as GPIO
import sys
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
count = 0
start = time.time()
def button_callback(channel):
    global count, start
    print("Pushed ", count)
    if(count == 0):
        start = time.time()
    count = count + 1
    
GPIO.add_event_detect(17, GPIO.RISING,
                      callback = button_callback,
                      bouncetime = 133)
while True:
    message = input("q Quits, r shows RPM and resets count: ")
    if(message == "q"):
        GPIO.cleanup()
        sys.exit(0)
    elif(message == "r"):
        if(count == 0):
            print("0 RPM")
        else:
            elapsed = time.time() - start
            rpm = int(60 * count / elapsed)
            print(rpm, " RPM")
            start = time.time()
            count = 0
    else:
        print("Doofus")
GPIO.cleanup()
