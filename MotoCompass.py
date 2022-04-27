#MotorCompass for mpu9250
import RPi.GPIO as GPIO
import time
import statistics as stats
import MotorControl as Control
from mpu9250_i2c import *
import smbus,time,datetime
import numpy as np
import matplotlib.pyplot as plt
import math as Math

mpu6050_vec,AK8963_vec,t_vec,Av = [],[],[],[]
numExcept = 0
t1 = time.time()    
motorLeft = Control.MotorControl(18, 9, 10)
motorRight = Control.MotorControl(19, 7, 8)
# code to check that the motors are running
ii = 100
while(True):
    motorLeft.fwd(50)
    motorRight.fwd(50)
    #take abunch of mpu 9250 readings
    print('recording data')
    sample_time = 0.1
    for iii in range(0,ii):
        tlast = time.time()
        try:
            ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
            mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data
        except:
            numExcept = num_except + 1
            continue
        while ((time.time() - tlast) < sample_time):
            continue#delay til sample time over
        t_vec.append(time.time()) # capture timestamp
        AK8963_vec.append([mx,my,mz])
        mpu6050_vec.append([ax,ay,az,wx,wy,wz])

    motorLeft.stop()
    motorRight.stop()
    motorLeft.quit()#quits all because it does cleanup
    #wish I knew how to get rid of the red dot
    print('sample rate accel: {} Hz'.format(ii/(time.time()-t1))) # print the sample rate
    print('# except: {}'.format(numExcept))
    t_vec = np.subtract(t_vec,t_vec[0])
    for i in range (0,ii):
        Av = AK8963_vec[i]
        hd = Math.atan2(Av[1],Av[0])*(180/Math.pi)
        print(Av, '{0:.3f}'.format(hd))
    time.sleep(1)
    exit()
#end of while
# #the real code starts here
# #first get the direction we are pointing
# dir = 0
# sumDirs = 0.0
# dirs = []
# numAvg = 6
# initVel = 30
# checkVel = 2* initVel #adjust vel. if v<2*inv, +lV 
# rightVel = initVel
# leftVel = initVel
# dur = 10
# trackDif = 1
# adj = 1#how much to adjust spped
# #operator should point buggy at target
# for i in range (numAvg):
#     (deg,min) = hmc.getHeading()
#     dirs.append(deg+min/60)
#     sumDirs = sumDirs + dirs[i]
#     time.sleep(0.1)
# dir = sumDirs/numAvg #dir = target heading standing still
# x = input()
# if(x == 'g'):#go
#     start = time.time()
#     done = False
#     motorLeft.fwd(leftVel)
#     motorRight.fwd(rightVel)
#     sumVels = leftVel + rightVel
#     dirLst = []
#     dirIdx = 0
#     #this code will not work if dir is approx due north
#     #need special code (tbd) for that case
#     #for now, point car toward south
#     while (time.time() - start) < dur:
#         time.sleep(0.1)
#         (deg, min) = hmc.getHeading()
#         nowDir = deg + min/60
#         dirIdx += 1
#         difHead = nowDir - dir
#         if (abs(difHead) > trackDif):
#             if (difHead > 0):#tells which way to go
#                 if(sumVels > checkVel):
#                     #left wheel needs to slow down
#                     leftVel = leftVel - adj * difHead
#                     motorLeft.fwd(leftVel)
#                 else:
#                     #right wheel needs to speed up
#                     rightVel = rightVel + adj * difHead
#                     motorRight.fwd(rightVel)
# #This stuff could be simplified
#             else:#current heading - target <= 0
#                 if(sumVels > checkVel):
#                     #right wheel needs to slow down
#                     rightVel = rightVel - adj * difHead
#                     motorRight.fwd(rightVel)
#                 else:
#                     #left wheel needs to speed up
#                     leftVel = leftVel + adj * difHead
#                     motorLeft.fwd(leftVel)
#             #do nothing if nowDir close to dir
#         sumVels = rightVel + leftVel
#         dirLst.append([round(nowDir,2),
#                        round(leftVel,2),
#                        round(rightVel,2)])
#     motorLeft.stop()
#     motorRight.stop()
#     for elem in dirLst:
#         print(elem)
# if(x == 'q'):
#     motorLeft.stop()
#     motorRight.stop()
#     motorLeft.quit()
#     exit()
            
            
            
    
    

