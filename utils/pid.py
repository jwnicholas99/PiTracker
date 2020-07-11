import time

class PID:
    def __init__(self, kP=1, kI=0, kD=0):
        self.kP= kP
        self.kI = kI
        self.kD = kD

    def initialize(self):
        # initialize current and previous time
        self.curTime = time.time()
        self.prevTime = self.curTime

        # init previous error
        self.prevError = 0

        # init term result vars
        self.cP = 0
        self.cI = 0
        self.cD = 0

    def update(self, error, sleep=0.5):
        # give some time for action
        time.sleep(sleep)

        # calculate change in time
        self.curTime = time.time()
        deltaTime = self.curTime - self.prevTime

        # delta error
        deltaError = error - self.prevError

        # Proportional (P) term
        self.cP = error

        # Integral (I) term
        self.cI += error * deltaTime

        # Derivative (D) term
        self.cD = (deltaError / deltaTime) if deltaTime > 0 else 0

        # save parameters of curr state for next calc
        self.prevTime = self.curTime
        self.prevError = error

        # return sum of terms
        return self.kP * self.cP + self.kI * self.cI + self.kD * self.cD
