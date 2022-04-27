#Testcv4.py Looda for circles finds center


import sys
import cv2 as cv
import numpy as np
import time

def getTimeInMillis():
    return (int)(time.time()*1000.0)

def main():
   
    filename = 'Redlight13on.jpg'
    
    # Loads an image
    #src = cv.imread(filename, cv.IMREAD_COLOR)
    imageOrig = cv.imread("Redlight13on.jpg")
    scale = 0.25
    h = int(scale * imageOrig.shape[0]) 
    w = int(scale * imageOrig.shape[1])
    src = cv.resize(imageOrig, (w, h))
    print ("resized to: w = ", w, ", h = ",h) 
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        #print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1
    cv.imshow("Scaled image",src)
    cv.waitKey(0)
    cv.destroyAllWindows()
   
   
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    cv.imshow("Grayed image",gray)
    cv.waitKey(0)
    cv.destroyAllWindows()
   
   
    gray = cv.medianBlur(gray, 5)
    cv.imshow("Blured image",gray)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    ret, binary = cv.threshold(gray, 100, 255, 
      cv.THRESH_OTSU)
    binary = gray
    cv.imshow("Binary image",binary)
    cv.waitKey(0)
    cv.destroyAllWindows()

   
   
    rows = binary.shape[0]
    start = getTimeInMillis()
    circles = cv.HoughCircles(binary, cv.HOUGH_GRADIENT, 1, rows / 8,
                               param1=205, param2=8,
                               minRadius=20, maxRadius=324)
    computeTime = getTimeInMillis()- start
   
    print("Compute time = ",computeTime)   
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(src, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(src, center, radius, (255, 0, 255), 3)
    else:
        print ("No circles found")   
   
    cv.imshow("detected circles", src)
    cv.waitKey(0)
    cv.destroyAllWindows()
   
    return 0
if __name__ == "__main__":
    main()

