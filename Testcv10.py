#Testcv10: Figuring out how to do buggy self control: seems screwn
import RPi.GPIO as GPIO
import sys
from time import sleep
import time
import pigpio
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

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
        self.speed = 99
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
#        if(speed != self.speed):
        self.speed = speed
        self.pw.ChangeDutyCycle(speed)
        print ("dtcy: ",speed)
        self.dir=1   #forward
        print("f", speed)

    def bck(self, speed):
        GPIO.setmode(GPIO.BCM)

        GPIO.output(self.motorPin2,GPIO.HIGH)
        GPIO.output(self.motorPin1,GPIO.LOW)
#         if(speed != self.speed):
        self.speed = speed
        self.pw.ChangeDutyCycle(speed)
        self.dir=0   #back
        print("bspd: ",self.speed)
        
    def adj(self, deg):
        self.speed += deg
        self.bck(self.speed)
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
#class to do control of the two wheels independently
class carBasic():
    def __init__(self, en1, pin1, pin2, en2, pin3,pin4):
        GPIO.setmode(GPIO.BCM)
        self.ml = MotorControl(en1, pin1, pin2)
        self.mr = MotorControl(en2, pin3, pin4)
    def motorsSpeed(self, left, right):
        self.speedleft = left
        self.speedright = right
        
    def go(self):
        GPIO.setmode(GPIO.BCM)
        self.ml.bck(self.speedleft)
        self.mr.bck(self.speedright)
    
    def adjLeft(self,delta):
        self.delta = delta
        self.ml.adj(self.delta)
        print("l ",self.delta)
        
    def adjRight(self,delta):
        self.delta = delta
        self.mr.adj(self.delta)
        print("r ",self.delta)
        
    def stop(self):
        GPIO.setmode(GPIO.BCM)
        self.ml.stop()
        self.mr.stop()

    def quit(self):
        GPIO.setmode(GPIO.BCM)
        self.stop()
        GPIO.cleanup()
        
#routine to get the light on center and start the camera
def initCamera(center):
    rawCapture = PiRGBArray(camera)
    # allow the camera to warmup
    time.sleep(3)
    camera.resolution = (512, 384)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    # display the image on screen and wait 3 secs
    cv2.imshow("Image", image)
    cv2.waitKey(3000)
    destroyAllWindows()
    #   set up masks
    WHITE_MIN = np.array([239, 239, 239],np.uint8)
    WHITE_MAX = np.array([255, 255, 255],np.uint8)

    frame_threshed = cv2.inRange(src, WHITE_MIN, WHITE_MAX)
    cv2.imshow('white image', frame_threshed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ret, binary = cv2.threshold(frame_threshed, 100, 255, 
      cv2.THRESH_OTSU)
    inverted_binary = ~binary
camera = PiCamera()
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(2)
# grab the first image from the camera
camera.resolution = (512, 384)
camera.capture(rawCapture, format="bgr")
image = rawCapture.array
# display the image on screen and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(3000)
cv2.destroyAllWindows()
dist = 100
while dist > 0:
    fname = "/home/pi/Develop/Images/" + "c" + str(dist) + ".jpg"
    
    camera.resolution = (512, 384)
    camera.capture(fname)
#    img = cv2.imread(fname)
#    cv2.imshow(fname,img)
#    cv2.waitKey(500)
#    sleep(0.2)
    dist = dist - 10
#    cv2.destroyAllWindows()
    

    
#rawCapture = PiRGBArray(camera)
# allow the camera to warmup
#camera.capture(rawCapture, format="bgr")
#image = rawCapture.array
# display the image on screen and wait for a keypress
#cv2.imshow("Image", image)
#cv2.imwrite("/home/pi/Develop/Images/" + "x" + ".jpg", image)
#cv2.waitKey(0)
cv2.destroyAllWindows()
    

    
    
        

