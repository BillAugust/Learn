#Testcv12 Try to combine camera and motors
# import the necessary packages
import sys
from time import sleep
import time
import RPi.GPIO as GPIO
import pigpio
from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import cv2
import numpy as np

fwdadjust = 0
bckadjust = 0
turnspd = 30
rtTime = 1.4
ltTime = 1.28
ltTimeAdj = 0.0
rtTimeAdj = 0.0

#servo constants

def getTimeInMillis():
    return (int)(time.time()*1000.0)

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
        #print("bspd: ",self.speed)
    
    def curSpeed(self):
        return self.speed
        
    def adj(self, deg):
        self.speed += deg
        if(self.speed >= 99):
            self.speed = 99
        if(self.speed < 0):
            self.speed = 0
        #print("spd ", self.speed, " deg ", deg)
        self.bck(self.speed)
                        
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
class CarBasic():
#a static table used by the correct function
    global corTable
    
#       5:0,20:1,50:2,100:3,150:4,320:101}
    
    def __init__(self, en1, pin1, pin2, en2, pin3,pin4):
        GPIO.setmode(GPIO.BCM)
        self.ml = MotorControl(en1, pin1, pin2)
        self.mr = MotorControl(en2, pin3, pin4)
        self.oldret = 0

    def motorsSpeed(self, left, right):
        self.speedleft = left
        self.speedright = right
        
    def go(self):
        GPIO.setmode(GPIO.BCM)
        #back cause cam points rear
        self.ml.bck(self.speedleft)
        self.mr.bck(self.speedright)
    
    def adjLeft(self,delta):
        self.delta = delta
        self.ml.adj(self.delta)
        #print("l ",self.delta)
        
    def adjRight(self,delta):
        self.delta = delta
        self.mr.adj(self.delta)
        print("r ",self.delta)
    
    def curSpeed(self):
        return self.ml.curSpeed(), self.mr.curSpeed()
        
    def stop(self):
        GPIO.setmode(GPIO.BCM)
        self.ml.stop()
        self.mr.stop()

    def quit(self):
        GPIO.setmode(GPIO.BCM)
        self.stop()
        GPIO.cleanup()
    
    #Returns the correcton value based on the offset
    #This may change a lot based on experience
    corTable = np.array([[5,0],[20,1],
                         [30,2],[40,3],
                         [50,4],[80,5],
                         [300,5],[301,101]],np.int32)
    def correct(self, offset):
        sign = 1
        absOff = abs(offset)
        if absOff > offset:
            sign = -1
        ret = 101
        for i in range(len(corTable)):
            if (absOff <= corTable[i,0]):
                ret = sign * corTable[i,1]
                break
        if self.oldret == ret:
            return 0
        else:
            self.oldret = ret
        
        return ret


#old correct() code ; may turn out useful       
#Old 1       absOff = abs(offset)
#        sign = 1
#        if absOff > offset:
#            sign = -1
#        ret = 101
#        for i in range(len(corTable)):
#            if (absOff <= corTable[i,0]):
#                ret = corTable[i,1]
#                break
#        return sign * ret

        
            
#old1            
#        absOff = abs(offset)
#        if(absOff < okay) ret = 0
#        elif(absOff < smallCorrect)ret = 1
#        absOff = abs(offset)
#       sign = offset/abs(offset)
#       ret = int(100/320 * offset)
        #print(ret)
#        return ret

class stats():
    def __init__(self, index, timeStamp,
                 offset, correct,
                 speedLeft, speedRight):
        self.index = index
        self.timeStamp = timeStamp
        self.offset = offset
        self.correct = correct
        self.speedLeft = speedLeft
        self.speedRight = speedRight
        #print (correct)
    def printStats():
        print(
            "Index: ",self.index,
            "Time: ",self.timeStamp,
            "Offset: ",self.offset,
            "Correct: ",self.correct,
            "SpdLft: ",self.speedLeft,
            "SpdRgt: ",self.speedRight)
        

startTime = getTimeInMillis()    
print("Start at: ",startTime)
import numpy as np
notCentered = True
#picamera.PiCamera().close()
WHITE_MIN = np.array([239, 239, 239],np.uint8)
WHITE_MAX = np.array([255, 255, 255],np.uint8)
camResW = 640;camResH = 480
with picamera.PiCamera() as camera:
    camera.resolution = (camResW, camResH)      
    #camera.framerate = 10
    # allow the camera to warmup
    time.sleep(3)
    while notCentered:
        output = np.empty((camResH, camResW , 3), dtype = np.uint8)
        camera.capture(output, 'bgr')
        blank_image = np.zeros(output.shape,dtype=np.uint8)
#cv2.line(blank_image, (cx,0), (cx,camResH - 1), (255,0,0), 2)
        cv2.line(blank_image,(int(camResW/2),0),
                 (int(camResW/2),(int(camResH)) - 1),
                 (0,0,255), 2)
        no_image = blank_image
    #  d#T2sLst


#point car's camera toward light (manual for now)
#will tell when pointed
        cv2.imshow("Centering",output)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
        if key == ord("c"):
            notCentered = False
        frame_threshed = cv2.inRange(output, WHITE_MIN, WHITE_MAX)
    #frame_threshed = cv2.cvtColor(frame_threshed, cv2.COLOR_HLS2BGR)
        cv2.imshow('white image', frame_threshed)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    #rows = frame_threshed.shape[0]
        start = getTimeInMillis()
        contours, hierarchy = cv2.findContours(frame_threshed,
          cv2.RETR_TREE,
          cv2.CHAIN_APPROX_SIMPLE)
        computeTime = getTimeInMillis()- start

        print("Compute time = ",computeTime)   
maxLen = 0;idx = -1
for i in range(len(contours)):
    conSize = contours[i].size
    if (conSize>20):
        print (i, " ", conSize)
        if(conSize > maxLen):
            maxLen = conSize
            idx = i
        no_image = blank_image
        no_image = cv2.drawContours(no_image, contours, i,(255,0,255),3,cv2.LINE_8,hierarchy,0)
        cv2.imshow('detected contour', no_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
x, y, w, h = cv2.boundingRect(contours[idx])
cx = int(x + w/2)
print( 'x: ',x,' y: ',y, ' w: ',w, ' h: ',h,' c:',cx)
cv2.rectangle(blank_image,(x,y), (x+w,y+h), (255,0,0), 2)
cv2.line(blank_image, (cx,0), (cx,camResH - 1), (255,0,0), 2)
print("Offset: ", cx - camResW/2)
cv2.imshow('boxed', blank_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
#sys.exit(0)
#now the fun part: make the buggy go to the light
#gentlemen start your engines
car = CarBasic(18,7,8,19,9,10)
car.stop()
difList = []
statList = []
picList = []
with picamera.PiCamera() as camera:
    print("Hit a legal key: q, g, s, p")
    try:
        idx = -1
        k = input()
        if(k == 'q'):
            cv2.destroyAllWindows()
            sys.exit()
        elif(k == 's'):
            car.stop()
        elif(k == 'g'):
            goTime = getTimeInMillis()
            print("Go at: ", goTime - startTime)
            camera.resolution = (camResW, camResH)
            camera.framerate = 10
            rawCapture = PiRGBArray(camera,
                                    size=(camResW, camResH))
            # allow the camera to warmup
            time.sleep(2)
            # capture frames from the camera
            quit = False
            i = 0
            runStats = list()
            nFrames = 100
            conSize = 0
            curFrame = 0
            corK = 1.0
            car.motorsSpeed(25, 25)
            car.go()

            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
                image = frame.array
                picList.append(image)
                threshed = cv2.inRange(image, WHITE_MIN, WHITE_MAX)
                contours, h = cv2.findContours(threshed,
                  cv2.RETR_TREE,
                  cv2.CHAIN_APPROX_SIMPLE)
                maxLen = 0;idx = -1
                for i in range(len(contours)):
                    conSize = contours[i].size
                    if (conSize>20):
                        if(conSize > maxLen):
                            maxLen = conSize
                            idx = i
                rawCapture.truncate(0)
                if(idx != -1):
                    x, y, w, h = cv2.boundingRect(
                        contours[idx])
                    cx = int(x + w/2)#center of pic
                    
                    offset = cx - camResW/2
                    correct = car.correct(offset)
                    if(abs(correct )>= 99):
                        car.stop()
                        print("Stop: speed impossible")
                        break
                    speedLeft, speedRight = car.curSpeed()
                    
                    thisStat = stats(
                        curFrame,
                        getTimeInMillis() - goTime,
                        offset,
                        correct,
                        speedLeft,
                        speedRight)
                    runStats.append(thisStat)
                    #print("Cor: ", correct, "F",int(corK * correct))
                    if(correct != 0):#don't adjust if on track
                        lt = int(correct/2)
                        rt = - (correct - lt)
                        car.adjLeft(lt)
                        car.adjRight(rt)
                    
                curFrame = curFrame + 1
                        
                print(nFrames," Center: ", x + w/2)
                    #print(nFrames, " ConSize: ",conSize)
                    
                nFrames = nFrames - 1
                if(nFrames <= 0):
                    break
                kn = cv2.waitKey(1)
                if(ord('p') == kn):
                    k = 'p'
                    break
                if(ord('q') == kn):
                    k = 'q'
                    break
            
            camera.close()
            car.stop()
            
            for j in range(len(runStats)):
                r = runStats[j]
                print(r.index,
                      " t: ", r.timeStamp,
                      " off: ", r.offset,
                      " cor: ", r.correct,
                      " left: ", r.speedLeft,
                      " right: ", r.speedRight)
                fname = "home/pi/Develop/Images/pic"
                fname = fname + str(j) + ".png"
                cv2.imshow(fname,picList[j])
                kn = cv2.waitKey(0)
                if (kn == ord('q')):
                    break
                cv2.destroyAllWindows()
            car.quit()
            sys.exit()
    except KeyboardInterrupt:
        print("Emergency stop")
        camera.close()
        car.quit()
            
            
                
                
            
                        


