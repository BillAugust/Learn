#CheckMotor
from MotorControl import MotorControl
from CarBasic import CarBasic
import time
import sys
car = CarBasic(19,9,10,18,7,8)
motLeft = 60
motRight = 00
car.motorsSpeed(motLeft, motRight)
k = ' '
print("hit b, f, q followed by <cr>")
while(k != 'q'):
    k = input()
    if(k == 'q'):
        sys.exit()
    elif(k == 'b'):
        car.goBck()
    elif(k == 'f'):
        car.goFwd()
    else:
        continue
    time.sleep(10)
    car.stop()

    
    
    


