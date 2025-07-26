from config import *

class GameClock:

    def __init__(self):
        self.frameTick = 0  # The main clock tick of the game, increments at each frame (1/60 secs, 60 fps)
        self.pausedMoment = 0
        self.move = self.TimingType(MOVE_PERIOD_INIT)  # Drop and move(right and left) timing object
        self.fall = self.TimingType(STARTING_SPEED * (SPEED_MULTIPLIER ** STARTING_LEVEL))  # Free fall timing object
        self.clearAniStart = 0

    class TimingType:

        def __init__(self, framePeriod):
            self.preFrame = 0
            self.framePeriod = framePeriod

        def check(self, frameTick):
            if frameTick - self.preFrame > self.framePeriod - 1:
                self.preFrame = frameTick
                return True
            return False

    def pause(self):
        self.pausedMoment = self.frameTick

    def unpause(self):
        self.frameTick = self.pausedMoment

    def restart(self, level):
        self.frameTick = 0
        self.pausedMoment = 0
        self.move = self.TimingType(MOVE_PERIOD_INIT)
        self.fall = self.TimingType(STARTING_SPEED * (SPEED_MULTIPLIER ** level))
        self.clearAniStart = 0

    def update(self):
        self.frameTick = self.frameTick + 1