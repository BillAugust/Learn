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
ltTimeAdj = 0.0
rtTimeAdj = 0.0

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
import numpy as np
notCentered = True 
#picamera.PiCamera().close()
WHITE_MIN = np.array([239, 239, 239],np.uint8)
WHITE_MAX = np.array([255, 255, 255],np.uint8)
PINK_MIN = np.array([188, 177, 223],np.uint8)
PINK_MAX = np.array([218, 209, 255],np.uint8)
camResW = 640;camResH = 480
with picamera.PiCamera() as camera:
    camera.resolution = (camResW, camResH)      
    #camera.framerate = 10
    # allow the camera to warmup
    time.sleep(3)
    while notCentered:
        output = np.empty((camResH, camResW , 3), dtype = np.uint8)
        camera.capture(output, 'bgr')
        output = cv2.flip(output,-1)
        blank_image = np.zeros(output.shape,dtype=np.uint8)
#cv2.line(blank_image, (cx,0), (cx,camResH - 1), (255,0,0), 2)
        cv2.line(blank_image,(int(camResW/2),0),
                 (int(camResW/2),(int(camResH)) - 1),
                 (0,0,255), 2)
    #  d#T2sLst


#point car's camera toward light (manual for now)
#will tell when pointed
        cv2.imshow("Centering",output)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
        if key == ord("c"):
            notCentered = False
#        frame_threshed = cv2.inRange(output, WHITE_MIN, WHITE_MAX)
        frame_threshed = cv2.inRange(output, WHITE_MIN,
                                     WHITE_MAX)
    #frame_threshed = cv2.cvtColor(frame_threshed, cv2.COLOR_HLS2BGR)
        cv2.imshow('white image', frame_threshed)
        key = cv2.waitKey(0)
        print (key)
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
        no_image = cv2.drawContours(no_image,
                                    contours, i,
                                    (255,0,255),3,
                                    cv2.LINE_8,
                                    hierarchy,0)
        cv2.imshow('detected contour', no_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
x, y, w, h = cv2.boundingRect(contours[idx])
cx = int(x + w/2)
print( 'x: ',x,' y: ',y, ' w: ',w, ' h: ',h,' c:',cx)
cv2.rectangle(blank_image,(x,y), (x+w,y+h),
              (255,0,0), 2)
cv2.line(blank_image, (cx,0), (cx,camResH - 1),
         (255,0,0), 2)
print("Offset: ", cx - camResW/2)
cv2.imshow('boxed', blank_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#sys.exit(0)
#now the fun part: make the buggy go to the light
#gentlemen start your engines
car = CarBasic(18,7,8,19,9,10)
car.stop()
car.motorsSpeed(40 ,38)
difList = []
statList = []
picList = []
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
            goTime = getTimeInMillis() - goTime
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
                        car.adjLeft(lt)#comment out to 
                        car.adjRight(rt)#just see no adj
                    
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
            while(nFrames > 0):
               picList.append(blank_image)
               nFrames = nFrames -1
            for j in range(len(runStats)):
                r = runStats[j]
                ostr = str(r.timeStamp)+ " "
                ostr = ostr + str(r.offset) + " "
                ostr = ostr + str(r.correct) + " "
                ostr = ostr + str(r.speedLeft) + " "
                ostr = ostr + str(r.speedRight)
#                 print (ostr)
                
                
#                     " t: ", r.timeStamp,
#                      " off: ", r.offset,
#                      " cor: ", r.correct,
#                      " left: ", r.speedLeft,
#                      " right: ", r.speedRight)
                fdir = "/home/pi/Develop/Learn/images"
                fname = "pic" + str(j) + ".png"
                xco = int(r.offset + camResW/2)
                cv2.line(picList[i],
                         (xco, 0),
                         (xco ,camResH - 1),
                         (255,0,0), 2)
                rotImg = picList[i]
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
#                kn = cv2.waitKey(0)c
                if (kn == ord('q')):
                    break
                cv2.destroyAllWindows()
            car.quit()
            sys.exit()
    except KeyboardInterrupt:
        print("Emergency stop")
        camera.close()
        car.quit()
            
            
                
                
            
                        


