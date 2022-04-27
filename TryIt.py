import MotorController

print("Starting motor control")

mc = MotorControl(18, 7,8)
while True:
    x = input("")
    if x=='f':
        mc.fwd(25)
    elif x=='s':
        mc.stop()
    elif x=='q':
        mc.stop()
        mc.quit()
        break

    else:
        print ("doofus")

