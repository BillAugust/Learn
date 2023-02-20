from MotorControl import MotorControl as Motor
import RPi.GPIO as GPIO
import pigpio
import time
import sys
leftEncPin = 27
rightEncPin = 22
whlLeft = Motor(7, 8, 18, leftEncPin)
whlRight = Motor(10, 9, 19, rightEncPin)
print(whlLeft.read())