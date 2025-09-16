from MainBoard import MainBoard

class Challenge_Spin(MainBoard):
    def __init__(self, starting_level, score, rotate_delay=10, upgrades=None):
        # upgrades und ghost_piece an das Elternboard weiterreichen
        super().__init__(starting_level, score, upgrades)
        self.updateSpeed()
        self.rotate_delay = rotate_delay
        self.frame_count = 0

    def rotate_CC(self):
        if self.frame_count % self.rotate_delay == 0:
            self.piece.rotate('CW')

    def rotate_cCC(self):
        self.frame_count += 1
