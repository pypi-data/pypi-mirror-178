class CalculateGoalPosition():
    def __init__(self, FingerLeftRangeMin, FingerLeftRangeMax, FingerRightRangeMin, FingerRightRangeMax):
        self._fingerLeftRangeMin = FingerLeftRangeMin
        self._fingerLeftRangeMax = FingerLeftRangeMax
        self._fingerRightRangeMin = FingerRightRangeMin
        self._fingerRightRangeMax = FingerRightRangeMax


    def Fingers(self, angleLeft, angleRight):
        GoalLeft = self.LeftFinger(angleLeft)
        GoalRight = self.RightFinger(angleRight)
        return GoalLeft, GoalRight

    def LeftFinger(self, angle):
        return self._Interpolation(self._fingerLeftRangeMin, self._fingerLeftRangeMax, angle)
    def RightFinger(self, angle):
        return  self._Interpolation(self._fingerRightRangeMin, self._fingerRightRangeMax, angle)
    def _Interpolation(self, min, max, goalPos):
        return (max - min) * goalPos + min
