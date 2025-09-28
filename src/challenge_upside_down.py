from __future__ import annotations
from MainBoard import MainBoard
from config import LIGHT_GRAY, blockColors, fontTitle, fontVersion, fontPAUSE, fontGAMEOVER


class Challenge_Upside_Down(MainBoard):
    def __init__(self, starting_level: int, score: int, upgrades=None):
        super().__init__(starting_level, score, upgrades)
        self.updateSpeed()

    def _flip_row(self, row: int) -> int:
        return (self.rowNum - 1) - row

    def rotate_CC(self):
        super().rotate_cCC()

    def rotate_cCC(self):
        super().rotate_CC()

    def draw_GAMEBOARD_CONTENT(self):
        from config import BLACK, GRAY
        from shared import gameDisplay

        if self.gameStatus == 'firstStart':
            titleText = fontTitle.render('TETRIS', False, (255, 255, 255))
            gameDisplay.blit(titleText, (self.xPos + 1.55 * self.blockSize, self.yPos + 8 * self.blockSize))

            versionText = fontVersion.render('v 2.0', False, (255, 255, 255))
            gameDisplay.blit(versionText, (self.xPos + 7.2 * self.blockSize, self.yPos + 11.5 * self.blockSize))
            return

        for row in range(self.rowNum):
            for col in range(self.colNum):
                flip_r = self._flip_row(row)
                if self.blockMat[row][col] == 'empty':
                    self.erase_BLOCK(self.xPos, self.yPos, flip_r, col)
                else:
                    self.draw_BLOCK(self.xPos, self.yPos, flip_r, col, blockColors[self.blockMat[row][col]])

        if self.piece.status == 'moving':
            if self.ghost_block:
                ghostPositions = self.piece.calculateGhostPosition()
                for i in range(4):
                    self.draw_BLOCK(
                        self.xPos,
                        self.yPos,
                        self._flip_row(ghostPositions[i]),
                        self.piece.blocks[i].currentPos.col,
                        LIGHT_GRAY,
                    )
            for i in range(4):
                self.draw_BLOCK(
                    self.xPos,
                    self.yPos,
                    self._flip_row(self.piece.blocks[i].currentPos.row),
                    self.piece.blocks[i].currentPos.col,
                    blockColors[self.piece.type],
                )

        for row in range(self.rowNum + 1):
            import pygame
            pygame.draw.line(
                gameDisplay, GRAY,
                (self.xPos, self.yPos + row * self.blockSize),
                (self.xPos + self.colNum * self.blockSize, self.yPos + row * self.blockSize), 1
            )
        for col in range(self.colNum + 1):
            import pygame
            pygame.draw.line(
                gameDisplay, GRAY,
                (self.xPos + col * self.blockSize, self.yPos),
                (self.xPos + col * self.blockSize, self.yPos + self.rowNum * self.blockSize), 1
            )

        if self.gamePause:
            import pygame
            pygame.draw.rect(gameDisplay, (80, 80, 80),
                             [self.xPos + self.blockSize, self.yPos + 8 * self.blockSize, 8 * self.blockSize, 4 * self.blockSize], 0)
            pauseText = fontPAUSE.render('PAUSE', False, (0, 0, 0))
            gameDisplay.blit(pauseText, (self.xPos + 1.65 * self.blockSize, self.yPos + 8 * self.blockSize))

        if self.gameStatus == 'gameOver':
            import pygame
            pygame.draw.rect(gameDisplay, (150, 150, 150),
                             [self.xPos + self.blockSize, self.yPos + 8 * self.blockSize, 8 * self.blockSize, 8 * self.blockSize], 0)
            gameOverText0 = fontGAMEOVER.render('GAME', False, (0, 0, 0))
            gameDisplay.blit(gameOverText0, (self.xPos + 2.2 * self.blockSize, self.yPos + 8 * self.blockSize))
            gameOverText1 = fontGAMEOVER.render('OVER', False, (0, 0, 0))
            gameDisplay.blit(gameOverText1, (self.xPos + 2.35 * self.blockSize, self.yPos + 12 * self.blockSize))
