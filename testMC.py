#test file
import MotorControl as Control
import RPi.GPIO as GPIO
print("Starting motor control")

mcl = Control.MotorControl(18, 9, 10)
mcr = Control.MotorControl(19, 7, 8)
while True:
    x = input("")
    if x=='f':
        mcl.fwd(50)
        mcr.fwd(50)
    elif x=='s':
        mcl.stop()
        mcr.stop()
    elif x=='q':
        mcl.quit()
        mcr.quit()
        GPIO.cleanup()

        break

    else:
        print ("doofus")
