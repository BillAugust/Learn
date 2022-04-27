#Testcv11: Trying to determine camera speed
import time
import picamera
import picamera.array
import cv2
import os

with picamera.PiCamera() as camera:
    camera.resolution = (256, 192)
    camera.start_preview()
    time.sleep(3)
    imagel = list()
    dist = 10
    start = time.time()
#    print ("Start: ", start)
#    with picamera.array.PiRGBArray(camera) as stream:
    
    t1=0
    t2=0
    while dist > 0:
        with picamera.array.PiRGBArray(camera) as stream:
            t1 = time.time()
            camera.capture(stream, format = 'bgr')
            t2 = time.time()
            imagel.append(stream.array)
        dist = dist - 1
    print ("Elapsed: ", time.time() - start)
    print ("t1: ", t1, " t2: ", t2, " dif: ", t2 - t1)
    while dist < 10:
        image = imagel[dist]
        cv2.imshow(str(dist),image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        dist = dist + 1
    cv2.destroyAllWindows()
