#CreepCar  Tries to get an ide fo how to control car
#through running one wheel and then the other.
import sys
from time import sleep
import time
import RPi.GPIO as GPIO
import pigpio
from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
from MotorControl import MotorControl
from CarBasic import CarBasic
import os
import cv2
import numpy as np

def getTimeInMillis():
    return (int)(time.time()*1000.0)


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
        
with picamera.PiCamera() as camera:
    print("Hit a legal key: q, g, s, p, then<cr>")
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
            nFrames = 30
            conSize = 0
            curFrame = 0
            corK = 1.0
            car.goFwd()
            creepl = 0.1
            creepr = 0.1
            for frame in camera.capture_continuous(
                rawCapture,
                format="bgr",
                use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
                image = frame.array
                picList.append(image)
                threshed = cv2.inRange(image,
                                       WHITE_MIN,
                                       WHITE_MAX)
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
                    cx = int(x + w/2)#w/2 is contour center                    
                    offset = cx - camResW/2
                    if offset > 0:
                        speedLeft = 0
                        speedRight = 40
                        timeToCreep = int(creepR*offset)+500
                    else:
                        speedLeft = 40
                        speedRight = 0
                        timeToCreep = int(creepL*offset)+500

                    correct = car.correct(offset)
                    print("cx: ",cx,
                          " off: ",offset,
                          " cor ",correct)
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
                        lt = (correct/2)
                        rt = - (correct - lt)
                        print("lt: ",lt,"rt: ",rt)
#                        car.adjLeft(lt)#comment out to 
#                        car.adjRight(rt)#just see no adj
                    
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
        


