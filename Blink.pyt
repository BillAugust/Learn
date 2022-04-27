import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 100)  
dc=0                               # set dc variable to 0 for 0%
pwm.start(dc)                      # Start PWM with 0% duty cycle

try:
  while True:                      # Loop until Ctl C is pressed to stop.
    for dc in range(0, 101, 5):    # Loop 0 to 100 stepping dc by 5 each loop
      pwm.ChangeDutyCycle(dc)
      time.sleep(0.05)             # wait .05 seconds at current LED brightness
    for dc in range(95, 0, -5):    # Loop 95 to 5 stepping dc down by 5 each loop
      pwm.ChangeDutyCycle(dc)
      time.sleep(0.05)             # wait .05 seconds at current LED brightness
      print(dc)
except KeyboardInterrupt:
  print("Ctl C pressed - ending program")

pwm.stop()                         # stop PWM
GPIO.cleanup()                     # resets GPIO ports used back to input mode
