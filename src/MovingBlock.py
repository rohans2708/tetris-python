class MovingBlock:

    def __init__(self):
        self.currentPos = self.CurrentPosClass(0, 0)
        self.nextPos = self.NextPosClass(0, 0)

    class CurrentPosClass:

        def __init__(self, row, col):
            self.row = row
            self.col = col

    class NextPosClass:

        def __init__(self, row, col):
            self.row = row
            self.col = col