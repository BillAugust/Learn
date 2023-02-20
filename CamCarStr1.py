#CamCarStr
#try to go straight
#CamMotor
#Try to test combined camera and motors for way to
#control straightness. Much code stolen from CamMotor.py

# import the necessary packages
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

difList = []
statList = []
picList = []
runStats = []

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

timeStart = getTimeInMillis()    
print("Start at: ",timeStart)
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
            speedLeft = 45
            speedRight = 42
            car.motorsSpeed(speedLeft ,speedRight)
            break
    try:
        while True:
            goTime = getTimeInMillis()
            print("Go at: ", goTime - timeStart)
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
            timeStart = time.time()
            quit = False
            i = 0
            runStats = list()
            totFrames = 50
            nFrames = totFrames
            conSize = 0
            curFrame = 0
            #gentlemen start your engines
            car.goFwd()
            for frame in camera.capture_continuous(
                rawCapture,
                format="bgr",
                use_video_port=True):#roll cameras
            # grab the raw NumPy array  image,
            # then initialize the timestamp
                timeStamp = time.time() - timeStart
                timeStamp = int(1000*timeStamp) / 1000.0
                image = cv2.rotate(frame.array,
                               cv2.ROTATE_180)
                picList.append(image)
                thisStat = stats(totFrames - nFrames,
                                timeStamp,
                                0,0,
                                speedLeft,
                                speedRight)
                runStats.append(thisStat)
                print(nFrames)
                nFrames = nFrames - 1
                if nFrames == 20:
                    speedLeft = speedLeft +10
                    car.motorsSpeed(speedLeft,
                                    speedRight)
                    car.goFwd()
                if(nFrames <= 0):
                    break
                cv2.imshow(" ",image)
                k = cv2.waitKey(1)
                if k == ord('q'):
                    car.stop()
                    print("q hit")
                    break
                rawCapture.truncate(0)
            camera.close()
            car.stop()
            print("stopping at ",len(runStats))
            #save the data in files for later review
            for j in range(len(runStats)):
                r = runStats[j]
                ostr = str(r.timeStamp)+ " "
                ostr = ostr + str(r.offset) + " "
                ostr = ostr + str(r.correct) + " "
                ostr = ostr + str(r.speedLeft) + " "
                ostr = ostr + str(r.speedRight)
                fdir = "/home/pi/Develop/Learn/images"
                fname = "pic" + str(j) + ".png"
                xco = int(r.offset + camResW/2)
                cv2.line(picList[j],
                         (xco, 0),
                         (xco ,camResH - 1),
                         (255,0,0), 2)
                rotImg = picList[j]
                cv2.putText(rotImg,
                            ostr,
                            (10,30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,(255,255,255),1,1)
#                cv2.imshow(fname,picList[j])
                curDir = os.getcwd()
                os.chdir(fdir)
                cv2.imwrite(fname, rotImg)
                os.chdir(curDir)
                kn = cv2.waitKey(1)
                if (kn == ord('q')):
                    break
                cv2.destroyAllWindows()
            print("App ending")
            car.quit()
            cv2.destroyAllWindows()
            sys.exit()
    except KeyboardInterrupt:
        print("Emergency stop")
        camera.close()
        car.quit()

