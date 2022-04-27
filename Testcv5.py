#Testcv5 Hough circles test.
import cv2
import numpy as np
import time

def getTimeInMillis():
    return (int)(time.time()*1000.0)


def main():
    filename = 'Redlight25on.jpg'
    
    # Loads an image
    imageOrig = cv2.imread(filename)
    scale = 0.25
    h = int(scale * imageOrig.shape[0]) 
    w = int(scale * imageOrig.shape[1])
    #scale the image down to 1/v for less process time
    src = cv2.resize(imageOrig, (w, h))
    cv2.imshow('scaled', src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ORANGE_MIN = np.array([5, 50, 100],np.uint8)
    ORANGE_MAX = np.array([15, 255, 255],np.uint8)

    hsv_img = cv2.cvtColor(src,cv2.COLOR_BGR2HSV)

    frame_threshed = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
    cv2.imshow('orange.jpg', frame_threshed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    rows = frame_threshed.shape[0]
    start = getTimeInMillis()
    circles = cv2.HoughCircles(frame_threshed, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=208, param2=21 ,
                               minRadius=10, maxRadius=324)
    computeTime = getTimeInMillis()- start
   
    print("Compute time = ",computeTime)   
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(frame_threshed, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv2.circle(frame_threshed, center, radius, (255, 0, 255), 3)
    else:
        print ("No circles found")   
   
    cv2.imshow("detected circles", frame_threshed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   
    return 0
if __name__ == "__main__":
    main()

