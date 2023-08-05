import unittest

from serial_fingers_control.CalculateGoalPosition import *
from serial_fingers_control.FingersControl import *

class FingersControlTest(unittest.TestCase):

    def testFingerControl(self):
        calc = CalculateGoalPosition(250, 600, 600, 250)
        pos = calc.LeftFinger(0.1)
        control = FingersControl()
        data = control.FingersManage(4, int(pos), 100)
        self.assertEqual([23, 4, 1, 29, 100, 196, 36], data)


if __name__ == '__main__':
    unittest.main()
