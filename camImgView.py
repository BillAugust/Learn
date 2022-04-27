#camImgViewer
import os
import cv2

global wd, inc, nfirst, strt
wd = "/home/pi/Develop/Images"
os.chdir(wd)
print(os.getcwd())
inc = 0
nfirst = 10
strt = 'c'
while True:
    print("What?")
    x = input("")
    if x=='d':
        print("new directory?")
        wdt=input("")
        if(wdt != ""):
            os.chdir(wdt)
        print("cwd = " + os.getcwd())
    elif x=='s':
        print("First Letter?")
        strt = input("")#first letter of fillename
    elif x=='f':
        firstDist = input("")#first distance in fname
        if(firstDist != ""):
            nfirst = int(firstDist)
    elif x=='p':#print first filename
        print(str(strt) + str(nfirst) +
              ".jpg") 
        
    elif x=='r':#show first file
        inc = 0
        endit = False
        while endit == False:
            fname = str(strt) + str(nfirst + inc) + ".jpg" 
            
            img = cv2.imread(fname)
            if(not os.path.isfile(fname)):
                endit = True
                print("No file ",fname)
                break
            cv2.imshow(fname,img)
            k = cv2.waitKey(0)
            print("key was:",k)
            cv2.destroyAllWindows()
            if k==110:#show next file
                inc = inc + 10
            else:endit = True
    elif x=='q':
        cv2.destroyAllWindows()
        break
print("Done")

    