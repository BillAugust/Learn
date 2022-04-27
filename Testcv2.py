import cv2 as cv
import sys
cv.samples.addSamplesDataSearchPath("/home/pi/opencv/samples/data")
img = cv.imread(cv.samples.findFile("starry_night.jpg"))
if img is None:
    sys.exit("Could not read the image.")
cv.imshow("Display window", img)
k = cv.waitKey(0)
if k == ord("s"):
    cv.imwrite("starry_night.png", img)
cv.destroyAllWindows()
    