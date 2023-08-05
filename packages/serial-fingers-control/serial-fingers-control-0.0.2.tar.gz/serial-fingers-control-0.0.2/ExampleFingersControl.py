import  time
from serial_fingers_control.FingersControl import *
from serial_fingers_control.CalculateGoalPosition import *

control = FingersControl()
calculate = CalculateGoalPosition(284, 563, 715, 562)

ServoID = 3
ServoID = 4

nullPosLeft = calculate.LeftFinger(0.0)
nullPosRight = calculate.RightFinger(0.0)
fullPosLeft = calculate.LeftFinger(1.0)
fullPosRight = calculate.RightFinger(1.0)

def Move(servo, pos):
    control.FingersManage(servo, int(pos), 100)


if __name__ == '__main__':
    Move(3, nullPosLeft)
    time.sleep(1)
    Move(4, nullPosRight)
    time.sleep(1)
    Move(3, fullPosLeft)
    time.sleep(1)
    Move(4, fullPosRight)
    time.sleep(1)





