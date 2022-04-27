#Testcv5
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
    #  d#T2sLst

    WHITE_MIN = np.array([239, 239, 239],np.uint8)
    WHITE_MAX = np.array([255, 255, 255],np.uint8)


    frame_threshed = cv2.inRange(src, WHITE_MIN, WHITE_MAX)
    #frame_threshed = cv2.cvtColor(frame_threshed, cv2.COLOR_HLS2BGR)
    cv2.imshow('white image', frame_threshed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #rows = frame_threshed.shape[0]
    start = getTimeInMillis()
    contours, hierarchy = cv2.findContours(frame_threshed,
      cv2.RETR_TREE,
      cv2.CHAIN_APPROX_SIMPLE)
    computeTime = getTimeInMillis()- start

    print("Compute time = ",computeTime)   
    if contours is not None:
        #circles = np.uint16(np.around(circles))
        for i in contours[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(frame_threshed, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv2.circle(frame_threshed, center, radius, (255, 0, 255), 3)
    else:
        print ("No contours found")   
   
    cv2.imshow("detected circles", frame_threshed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   
    return 0
if __name__ == "__main__":
    main()


