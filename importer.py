#importer
import os,sys
# current = os.getcwd()
# parent = os.path.dirname(current)
# sys.path.insert(0, parent)

import MotorControl
moto = MotorControl.MotorControl(1,2,3)
moto.stop()
input("Ret to exit")

moto.quit()