# Project: How to Detect and Draw Contours in Images Using OpenCV
# Author: Addison Sears-Collins
# Date created: February 28, 2021
# Description: How to detect and draw contours around objects in 
# an image using OpenCV.
 
import cv2 # Computer vision library
import numpy as np
import time
def getTimeInMillis():
    return (int)(time.time()*1000.0)

tstart = getTimeInMillis()
# Read the color image
try:
    imageOrig = cv2.imread("Redlight25on.jpg")
    scale = 0.25
    h = int(scale * imageOrig.shape[0]) 
    w = int(scale * imageOrig.shape[1])
    image = cv2.resize(imageOrig, (w, h))
    print ("resized to: w = ", w, ", h = ",h) 
    
    tend = getTimeInMillis()
    print("t0: ",tend-tstart)
    cv2.imshow('Reduced image', image)  
    cv2.waitKey(0) # Wait for keypress to continue

    
     
    # Make a copy
    new_image = image.copy()
    blank_image = image.copy()
    blank_image = np.zeros(new_image.shape,dtype=np.uint8)
    start1 = getTimeInMillis() 
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    end1 = getTimeInMillis()
    print ("I1: ",end1 - start1)
     
    # Display the grayscale image
    cv2.imshow('Gray image', gray)  
    cv2.waitKey(0) # Wait for keypress to continue
    cv2.destroyAllWindows() # Close windows
     
    # Convert the grayscale image to binary
    start2 = getTimeInMillis() 
    ret, binary = cv2.threshold(gray, 100, 255, 
      cv2.THRESH_OTSU)
    end2 = getTimeInMillis()
    print ("I2: ",end2 - start2)
     
    # Display the binary image
    cv2.imshow('Binary image', binary)
    cv2.waitKey(0) # Wait for keypress to continue
    cv2.destroyAllWindows() # Close windows
     
    # To detect object contours, we want a black background and a white 
    # foreground, so we invert the image (i.e. 255 - pixel value)
    start3 = getTimeInMillis() 
    inverted_binary = ~binary
    end3 = getTimeInMillis()
    print ("I3: ",end3 - start3)
    cv2.imshow('Inverted binary image', inverted_binary)
    cv2.waitKey(0) # Wait for keypress to continue
    cv2.destroyAllWindows() # Close windows
     
    # Find the contours on the inverted binary image, and store them in a list
    # Contours are drawn around white blobs.
    # hierarchy variable contains info on the relationship between the contours
    start4 = getTimeInMillis() 
    contours, hierarchy = cv2.findContours(inverted_binary,
      cv2.RETR_TREE,
      cv2.CHAIN_APPROX_SIMPLE)
    end4 = getTimeInMillis()
    print ("I4: ",end4 - start4)
         
    # Draw the contours (in red) on the original image and display the result
    # Input color code is in BGR (blue, green, red) format
    # -1 means to draw all contours
    with_contours = cv2.drawContours(image, contours, -1,(255,0,255),3)
    cv2.imshow('Detected contours', with_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
     
    # Show the total number of contours that were detected
    print('Total number of contours detected: ' + str(len(contours)))
     
    # Draw just the first contour
    # The 0 means to draw the first contour
    first_contour = cv2.drawContours(new_image, contours, 0,(255,0,255),3)
    cv2.imshow('First detected contour', first_contour)
    print("after First detected contour")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("after First detected contour wd")
     
    # Show all contours without original
    # The i means to draw the ith contour
    for i in range(len(contours)):
        if (contours[i].size>20):
            print (i, " ", contours[i].size)
            no_image = blank_image
            no_image = cv2.drawContours(no_image, contours, i,(255,0,255),3,cv2.LINE_8,hierarchy,0)
            cv2.imshow('detected contour', no_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        # Draw a bounding box around the first contour
    # x is the starting x coordinate of the bounding box
    # y is the starting y coordinate of the bounding box
    # w is the width of the bounding box
    # h is the height of the bounding box
    x, y, w, h = cv2.boundingRect(contours[0])
    cv2.rectangle(first_contour,(x,y), (x+w,y+h), (255,0,0), 5)
    cv2.imshow('First contour with bounding box', first_contour)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
     
    # Draw a bounding box around all contours
    for c in contours:
      x, y, w, h = cv2.boundingRect(c)
     
        # Make sure contour area is large enough
      if (cv2.contourArea(c)) > 10:
        cv2.rectangle(with_contours,(x,y), (x+w,y+h), (255,0,0), 5)
             
    cv2.imshow('All contours with bounding box', with_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

except KeyboardInterrupt:
    destroyAllWindows()
    image.close()