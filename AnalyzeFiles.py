#Analyze results of Testcv12_1
import cv2
import numpy
import sys   
done = False
idx = 0
bucket = list()
next = True
exp = 0
maxIdx = 99

while True:
    try:
        if next:
            if(idx > maxIdx):
                break
            fname = "/home/pi/Develop/Learn/images/"
            fname = fname + "pic" + str(idx) + ".png"
            bucket = cv2.imread(fname)
            cv2.imshow(fname, bucket)
        kn = cv2.waitKey(0)
        if (kn == ord('q')):
             break
        elif (kn == ord('i')):
            idx = 0
            exp = 0
            next = False
        elif ((kn >= ord('0')) and (kn <= ord('9'))):
            idx = (10 ** exp) * idx + kn - ord('0') 
            exp = exp + 1
            print (idx)
        else:
            if(next == True):
                idx = idx + 1
            next = True
            cv2.destroyAllWindows()

    except Exception as ex:
        print("Exception: ",ex)
        sys.exit()
sys.exit()    