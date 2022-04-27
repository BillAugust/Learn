#red13on
import cv2,os,time
path = "/home/pi/Desktop/Redlight13on.jpg"

print (path)
print(os.getcwd())
img = cv2.imread(path)
print(img.shape)

cv2.imshow("Red13on",img)

time.sleep(500)