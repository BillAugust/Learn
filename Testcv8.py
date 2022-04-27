# Testcv8 taking pics for distance analysis ;seems ok
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
# initialize the camera and grab a reference to the raw camera capture
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
dist = 170
while dist > 0:
    fname = "/home/pi/Develop/Images/" + "c" + str(dist) + ".jpg"
    
    camera.resolution = (512, 384)
    camera.capture(fname)
    time.sleep(10)
    img = cv2.imread(fname)
    cv2.imshow(fname,img)
    cv2.waitKey(2000)
    dist = dist - 10
    cv2.destroyAllWindows()
    

    
#rawCapture = PiRGBArray(camera)
# allow the camera to warmup
#camera.capture(rawCapture, format="bgr")
#image = rawCapture.array
# display the image on screen and wait for a keypress
#cv2.imshow("Image", image)
#cv2.imwrite("/home/pi/Develop/Images/" + "x" + ".jpg", image)
#cv2.waitKey(0)
cv2.destroyAllWindows()