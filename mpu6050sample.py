from mpu6050_i2c import *
import math as Math

time.sleep(5)

print('recording data')
a = 0
while a < 2:
    a = a + 1
    try:
        ax,ay,az,wx,wy,wz = mpu6050_conv()
        mx,my,mz = AK8963_conv()
    except:
        continue
    
    print('{}'.format('-'*30))
    print('accel [g]: x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(ax, ay, az))
    print('gyro [dps]: x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(wx, wy, wz))
    print('mag [uT]: x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(mx, my, mz))
    print('head [deg] h = {0:3.2f}'.format(Math.atan2(my/180, mx/180)*180.0))
    print('{}'.format('-'*30))
    time.sleep(1)
    