#Testcv6 This is screwn. But could be useful if errors were gone
import cv2
import numpy as np
import time
import os

def getTimeInMillis():
    return (int)(time.time()*1000.0)


def main():
    os.chdir('/home/pi/Develop/Images')
    filename = 'c170.jpg'
    
    # Loads an image
    imageOrig = cv2.imread(filename)
    scale = 1.0
    h = int(scale * imageOrig.shape[0]) 
    w = int(scale * imageOrig.shape[1])
    #scale the image down to 1/4 for less process time
    src = cv2.resize(imageOrig, (w, h))
    cv2.imshow('scaled', src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    blank_image = src.copy()
    blank_image = np.zeros(src.shape,dtype=np.uint8)
    no_image = blank_image
    #  d#T2sLst

    WHITE_MIN = np.array([239, 239, 239],np.uint8)
    WHITE_MAX = np.array([255, 255, 255],np.uint8)


    cv2.imshow('Detected contours', with_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    maxLen = 0
    idx = 0
    for i in range(len(contours)):
        conSize = contours[i].size
        if (conSize>10):
            print (i, " ", conSize)
            if(conSize > maxLen):
                maxLen = conSize
                idx = i
            no_image = blank_image
            no_image = cv2.drawContours(no_image, contours, i,(255,0,255),3,cv2.LINE_8,hierarchy,0)
            cv2.imshow('detected contour', no_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    # Get the bounding box of the contour with max size
    # x is the starting x coordinate of the bounding box
    # y is the starting y coordinate of the bounding box
    # w is the width of the bounding box
    # h is the height of the bounding box
    x, y, w, h = cv2.boundingRect(contours[idx])
    print( 'x = ',x,' y = ',y, ' w = ',w, ' h = ',h)
    cv2.rectangle(blank_image,(x,y), (x+w,y+h), (255,0,0), 1)
    cv2.imshow('boxed', blank_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return 0

if __name__ == "__main__":
    main()
