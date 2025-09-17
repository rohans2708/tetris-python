class GameKeyInput:

    def __init__(self):
        self.xNav = self.KeyName('idle', False)  # 'left' 'right'
        self.down = self.KeyName('idle', False)  # 'pressed' 'released'
        self.rotate = self.KeyName('idle', False)  # 'pressed' //KEY UP
        self.cRotate = self.KeyName('idle', False)  # 'pressed' //KEY Z
        self.enter = self.KeyName('idle', False)  # 'pressed' //KEY Enter
        self.pause = self.KeyName('idle', False)  # 'pressed' //KEY P
        self.restart = self.KeyName('idle', False)  # 'pressed' //KEY R
        self.hardDrop = self.KeyName('idle', False)  # NEU: //KEY SPACE
        self.hold = self.KeyName('idle', False)  # KEY H

    class KeyName:

        def __init__(self, initStatus, initTrig):
            self.status = initStatus
            self.trig = initTrig