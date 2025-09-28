from MainBoard import MainBoard
from src.config import *
from src.shared import gameDisplay, SCORES


class Challenge_No_Rows(MainBoard):
    def __init__(self, starting_level, score, pieces_to_place, upgrades=None):
        # upgrades-Dict an MainBoard übergeben
        super().__init__(starting_level, score, upgrades=upgrades)
        self.pieces_to_place = pieces_to_place
        self.score_per_piece = 100
        self.line_cleared = False
        self.updateSpeed()


    def checkAndApplyGameOver(self):
        # Lose condition: A row is completely filled
        if self.line_cleared:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music/stinger-2021-08-30_-_Boss_Time_-_www.FesliyanStudios.com.mp3")
            pygame.mixer.music.play()
            self.gameStatus = 'gameOver'
            return

        # Default behavior for game over
        if self.piece.gameOverCondition == True:
            self.gameStatus = 'gameOver'
            for i in range(0, 4):
                if self.piece.blocks[i].currentPos.row >= 0 and self.piece.blocks[i].currentPos.col >= 0:
                    self.blockMat[self.piece.blocks[i].currentPos.row][
                        self.piece.blocks[i].currentPos.col] = self.piece.type

    def updateScores(self):

        clearedLinesNum = 0
        self.pieces_to_place -= 1
        for i in range(0, 4):
            if self.clearedLines[i] > -1:
                clearedLinesNum += 1
                self.line_cleared = True


        self.score = self.score + self.score_per_piece
        if self.score > 999999:
            self.score = 999999

        if self.pieces_to_place <= 0:
            self.level += 1

    def draw_score_content(self, xPosRef, yLastBlock):
        positions = self._score_line_positions(yLastBlock, 6)
        # subtract 10 from each position
        positions = [pos - 10 for pos in positions]

        scoreText = fontSB.render('score:', False, TEXT_COLOR)
        gameDisplay.blit(scoreText, (xPosRef + self.blockSize, positions[0]))
        scoreNumText = fontSB.render(str(self.score), False, NUM_COLOR)
        gameDisplay.blit(scoreNumText, (xPosRef + self.blockSize, positions[1]))

        levelText = fontSB.render('level:', False, TEXT_COLOR)
        gameDisplay.blit(levelText, (xPosRef + self.blockSize, positions[2]))
        levelNumText = fontSB.render(str(self.level), False, NUM_COLOR)
        gameDisplay.blit(levelNumText, (xPosRef + self.blockSize, positions[3]))

        linesText = fontSB.render('blocks:', False, TEXT_COLOR)
        gameDisplay.blit(linesText, (xPosRef + self.blockSize, positions[4]))
        linesNumText = fontSB.render(str(self.pieces_to_place), False, NUM_COLOR)
        gameDisplay.blit(linesNumText, (xPosRef + self.blockSize, positions[5]))
