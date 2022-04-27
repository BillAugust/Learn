from i2clibraries import i2c_hmc5883l
import time
import statistics as stats
import MotorControl as Control
    
hmc =i2c_hmc5883l.i2c_hmc5883l(1)
hmc.setContinuousMode()
hmc.setDeclination(4, 0)
motorLeft = Control.MotorControl(18, 9, 10)
motorRight = Control.MotorControl(19, 7, 8)
# code to check that the motors are running
while(False):
    motorLeft.fwd(50)
    motorRight.fwd(50)
    #delay 15 secs
    time.sleep(15)
    motorLeft.stop()
    motorRight.stop()
    motorLeft.quit()#quits all because it does cleanup
    #wish I knew how to get rid of the red dot
    time.sleep(1)
    exit()
#end of while
#the real code starts here
#first get the direction we are pointing
dir = 0
sumDirs = 0.0
dirs = []
numAvg = 6
initVel = 30
checkVel = 2* initVel
rightVel = initVel
leftVel = initVel
dur = 10
trackDif = 1
adj = 1#how much to adjust spped
#operator should point buggy at target
for i in range (numAvg):
    (deg,min) = hmc.getHeading()
    dirs.append(deg+min/60)
    sumDirs = sumDirs + dirs[i]
    time.sleep(0.1)
dir = sumDirs/numAvg #dir = target heading standing still
x = input()
if(x == 'g'):#go
    start = time.time()
    done = False
    motorLeft.fwd(leftVel)
    motorRight.fwd(rightVel)
    sumVels = leftVel + rightVel
    dirLst = []
    dirIdx = 0
    #this code will not work if dir is approx due north
    #need special code (tbd) for that case
    #for now, point car toward south
    while (time.time() - start) < dur:
        time.sleep(0.1)
        (deg, min) = hmc.getHeading()
        nowDir = deg + min/60
        dirIdx += 1
        difHead = nowDir - dir
        if (abs(difHead) > trackDif):
            if (difHead > 0):#tells which way to go
                if(sumVels > checkVel):
                    #left wheel needs to slow down
                    leftVel = leftVel - adj * difHead
                    motorLeft.fwd(leftVel)
                else:
                    #right wheel needs to speed up
                    rightVel = rightVel + adj * difHead
                    motorRight.fwd(rightVel)
#This stuff could be simplified
            else:#current heading - target <= 0
                if(sumVels > checkVel):
                    #right wheel needs to slow down
                    rightVel = rightVel - adj * difHead
                    motorRight.fwd(rightVel)
                else:
                    #left wheel needs to speed up
                    leftVel = leftVel + adj * difHead
                    motorLeft.fwd(leftVel)
            #do nothing if nowDir close to dir
        sumVels = rightVel + leftVel
        dirLst.append([round(nowDir,2),
                       round(leftVel,2),
                       round(rightVel,2)])
    motorLeft.stop()
    motorRight.stop()
    for elem in dirLst:
        print(elem)
if(x == 'q'):
    motorLeft.stop()
    motorRight.stop()
    motorLeft.quit()
    exit()
            
            
            
    
    
