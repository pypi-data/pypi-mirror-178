import unittest
from serial_fingers_control.CalculateGoalPosition import *


class CalculateGoalPositionTest(unittest.TestCase):

    def testCalcLeftFinger(self):
        calc = CalculateGoalPosition(250, 600, 600, 250)
        pos = calc.LeftFinger(0.1)
        self.assertEqual(285.0, pos)

    def testCalcRightFinger(self):
        calc = CalculateGoalPosition(250, 600, 600, 250)
        pos = calc.RightFinger(0.1)
        self.assertEqual(565.0, pos)

    def testFingers(self):
        calc = CalculateGoalPosition(250, 600, 600, 250)
        pos = calc.Fingers(0.1, 0.1)
        self.assertEqual((285.0, 565.0), pos)


if __name__ == '__main__':
    unittest.main()
