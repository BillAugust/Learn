#ColorPic
#Takes a pic and saves it for analysis
import sys
from time import sleep
import time
import RPi.GPIO as GPIO
import pigpio
from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import os
import cv2
import numpy as np
camResW = 640;camResH = 480
with picamera.PiCamera() as camera:
    camera.resolution = (camResW, camResH)      
    #camera.framerate = 10
    # allow the camera to warmup
    time.sleep(3)
    output = np.empty((camResH, camResW , 3), dtype = np.uint8)
    camera.capture(output, 'bgr')
    blank_image = np.zeros(output.shape,dtype=np.uint8)
#cv2.line(blank_image, (cx,0), (cx,camResH - 1), (255,0,0), 2)
    cv2.imshow("Showing",output)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
    fdir = "/home/pi/Develop/Learn/images"
    fname = "colpic" + ".png"
    curDir = os.getcwd()
    os.chdir(fdir)
    cv2.imwrite(fname, output)
    os.chdir(curDir)
    
    sys.exit()
