#CamCarStr
#try to go straight
#CamMotor
#Try to test combined camera and motors for way to
#control straightness. Much code stolen from CamMotor.py

# import the necessary packages
import sys
..........................................................................................................................................................................................from time import sleep
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

difList = []
statList = []
picList = []

#servo constants

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

startTime = getTimeInMillis()    
print("Start at: ",startTime)
camResW = 640;camResH = 480
with picamera.PiCamera() as camera:
    camera.resolution = (camResW, camResH)
    # allow the camera to warmup
    time.sleep(3)
    while True:
        output = np.empty((camResH, camResW , 3),
                          dtype = np.uint8)
        camera.capture(output, 'bgr')
        cv2.imshow("Ready camera",output)

        key = cv2.waitKey(0)
        if key == ord('g'):
            car = CarBasic(18,7,8,19,9,10)
            car.stop()
            car.motorsSpeed(41 ,40)
            print("p1")
            break
    try:
        while True:
            goTime = getTimeInMillis()
            print("Go at: ", goTime - startTime)
            time.sleep(3)
            print("go")
            camera.resolution = (camResW, camResH)
            camera.framerate = 10
            # allow the camera to warmup
            time.sleep(2)
            rawCapture = PiRGBArray(camera,
                                    size=(camResW,
                                          camResH))
            # capture frames from the camera
            quit = False
            i = 0
            runStats = list()
            totFrames = 50
            nFrames = totFrames
            conSize = 0
            curFrame = 0
            corK = 1.0
            #gentlemen start your engines
            car.goFwd()
            for frame in camera.capture_continuous(
                rawCapture,
                format="bgr",
                use_video_port=True):#roll cameras
            # grab the raw NumPy array representing the image, then initialize the timestamp
                image = cv2.rotate(frame.array,
                               cv2.ROTATE_180)
                picList.append(image)
                nFrames = nFrames - 1
                print(nFrames)
                if(nFrames <= 0):
                    break
                cv2.imshow(" ",image)

                k = cv2.waitKey(1)
                if k == ord('q'):
                    car.stop()
                    break
#The following commented out for fact finding
#                elif k == ord('l'):
#                    car.adjRight(rtTimeAdj)#trn lft = more right
#                    print('l')
#                elif k == ord('r'):
#                    car.adjRight (-1*rtTimeAdj)#trn rt = less right
#                    print('r')
                    
                rawCapture.truncate(0)
            camera.close()
            car.stop()
            print("stopping")
            #save the data in files for later review
            fdir = "/home/pi/Develop/Learn/images"
            while(nFrames > 0):
                #blank remaining images if interrupted
                picList.append(blank_image)
                nFrames = nFrames  -1
            for ii in range (totFrames):
                fname = "pic" + str(ii) + ".png"
                curDir = os.getcwd()
                os.chdir(fdir)
                cv2.imwrite(fname, picList[ii])
                os.chdir(curDir)
            car.quit()
            sys.exit()
    except KeyboardInterrupt:
        print("Emergency stop")
        camera.close()
        car.quit()
