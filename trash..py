#trash.py probably useless code form testcv12 but who knows
sys.exit(0)


camera = PiCamera()
camera.resolution = (640, 480)
# capture frames from th e camera
quit = False
i = 0
images = list()
nFrames = 10
rawCapture = PiRGBArray(camera, size=(640, 480))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
# grab the raw NumPy array representing the image, then initialize the timestamp
# and occupied/unoccupied text
# and occupied/unoccupied text
    image = frame.array
#save first 10 images
    if i < nFrames:
#        print(i)
        images.append(image)
        i = i+1
    else:
        break
 
# show the frame
#    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
# clear the stream in preparation for the next frame
    rawCapture.truncate(0)
# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        quit = True
        break
    if key == ord("d"):
        break
cv2.destroyAllWindows()
if not quit:
    ii = 0
    while ii < 10:
        print(ii)
        cv2.imshow("Frame"+str(ii),images[ii])
        cv2.waitKey(0)
        ii = ii + 1
        cv2.destroyAllWindows()
cv2.destroyAllWindows()
    
        

