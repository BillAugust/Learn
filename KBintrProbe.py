#KBintrProbe
import time
dumList = list()
cnt = 0
start=time.time()
try:
    while True:   
        cnt += 1
        time.sleep(.4)
        dumList.append(int((time.time() - start)*100))
except KeyboardInterrupt:
    for i in range(len(dumList)):
        print (i, ": ", dumList[i]/100) 