#CamMotor
#Try to test combined camera and motors for way to
#control straightness

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

fwdadjust = 0
bckadjust = 0
turnspd = 30
rtTime = 1.4
ltTime = 1.28
ltTimeAdj = 5
rtTimeAdj = 5
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
notCentered = True
#picamera.PiCamera().close()
#WHITE_MIN = np.array([239, 239, 239],np.uint8)
#WHITE_MAX = np.array([255, 255, 255],np.uint8)
camResW = 640;camResH = 480
with picamera.PiCamera() as camera:
    camera.resolution = (camResW, camResH)      
    #camera.framerate = 10
    # allow the camera to warmup
    time.sleep(3)
    while notCentered:
        output = np.empty((camResH, camResW , 3),
                          dtype = np.uint8)
        camera.capture(output, 'bgr')
        blank_image = np.zeros(output.shape,
                               dtype=np.uint8)
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
        if key == ord('g'):
            notCentered = False
            car = CarBasic(19,9,10,18,7,8)
            car.stop()
            car.motorsSpeed(40 ,38)
            break
    try:
        while True:
            goTime = getTimeInMillis()
            print("Go at: ", goTime - startTime)
            time.sleep(3)
            print("go")
            camera.resolution = (camResW, camResH)
            camera.framerate = 10
            rawCapture = PiRGBArray(camera,
                                    size=(camResW,
                                          camResH))
            # allow the camera to warmup
            time.sleep(2)
            # capture frames from the camera
            quit = False
            i = 0
            runStats = list()
            totFrames = 30
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
                image = frame.array
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
                    





#code from Testcv12_1 which I may want later
##   #frame_threshed = cv2.cvtColor(frame_threshed, cv2.COLOR_HLS2BGR)
#         cv2.imshow('white image', frame_threshed)
#        key = cv2.waitKey(0)
#        print (key)
#        cv2.destroyAllWindows()
    #rows = frame_threshed.shape[0]
#        start = getTimeInMillis()
#        contours, hierarchy = cv2.findContours(frame_threshed,
#          cv2.RETR_TREE,
#          cv2.CHAIN_APPROX_SIMPLE)
#        computeTime = getTimeInMillis()- start

#        print("Compute time = ",computeTime)   
#maxLen = 0;idx = -1
#for i in range(len(contours)):
#    conSize = contours[i].size
#    if (conSize>20):
#        print (i, " ", conSize)
#        if(conSize > maxLen):
#            maxLen = conSize
#            idx = i
#        no_image = blank_image
#        no_image = cv2.drawContours(no_image,
#                                    contours, i,
#                                    (255,0,255),3,
#                                    cv2.LINE_8,
#                                    hierarchy,0)
#        cv2.imshow('detected contour', no_image)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
