import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)

soft_pwm = GPIO.PWM(13, 1)
soft_pwm.start(50)
input('Press_return_to_stop')
soft_pwm.stop()
GPIO.cleanup()