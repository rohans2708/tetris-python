from __future__ import annotations

import math
from MovingPiece import MovingPiece
from config import *
from shared import gameClock, gameDisplay, key, rng, SCORES


class MainBoard:

    def __init__(self, starting_level, score=0, upgrades: dict | None = None):

        # Size and position initiations
        self.blockSize = blockSize
        self.xPos = boardPosX
        self.yPos = boardPosX
        self.colNum = boardColNum
        self.rowNum = boardRowNum
        self.boardLineWidth = boardLineWidth
        self.blockLineWidth = blockLineWidth
        self.scoreBoardWidth = scoreBoardWidth

        # Matrix that contains all the existing blocks in the game board, except the moving piece
        self.blockMat = [['empty'] * boardColNum for i in range(boardRowNum)]

        self.piece = MovingPiece(boardColNum, boardRowNum, 'uncreated')

        self.lineClearStatus = 'idle'  # 'clearRunning' 'clearFin'
        self.clearedLines = [-1, -1, -1, -1]

        self.gameStatus = 'firstStart'  # 'running' 'gameOver'
        self.gamePause = False
        self.nextPieces = ['I', 'I']

        self.score = score
        self.level = starting_level
        self.lines = 0
        self.num_pieces = 0

        self.playerName = ""
        self.inputActive = False

        if upgrades is None:
            upgrades = {}
        self.upgrades_data = upgrades
        self.ghost_block = bool(self.upgrades_data.get("ghost_piece", 0))
        self.bomb_unlocked = bool(self.upgrades_data.get("bomb_block", 0))
        self.bomb_available = self.bomb_unlocked
        self.bomb_queued = False

        self.updateSpeed()
        self.relapse_keys()

    def perform_hard_drop(self):
        """
        Setzt das aktuelle Piece sofort auf die Ghost-Position und markiert es
        als 'collided', damit es noch im selben Frame gelockt und gewertet wird.
        """
        if self.piece.status != 'moving':
            return
        try:
            ghost_rows = self.piece.calculateGhostPosition()
            for i in range(4):
                # nur die Zeile auf die Ghost-Zeile setzen; Spalte bleibt
                self.piece.blocks[i].currentPos.row = ghost_rows[i]
            self.piece.status = 'collided'
        except Exception:
            # Falls irgendwas schiefgeht: ignoriere Hard-Drop
            pass

    def relapse_keys(self):
        key.down.trig = False
        key.down.status = 'released'
        key.cRotate.trig = False
        key.cRotate.status = 'released'
        key.rotate.trig = False
        key.rotate.status = 'released'
        key.bomb.trig = False
        key.bomb.status = 'released'

    def setPlayerName(self, name):
        self.playerName = name
    def restart(self):
        self.blockMat = [['empty'] * self.colNum for i in range(self.rowNum)]

        self.piece = MovingPiece(self.colNum, self.rowNum, 'uncreated')

        self.lineClearStatus = 'idle'
        self.clearedLines = [-1, -1, -1, -1]
        gameClock.fall.preFrame = gameClock.frameTick
        self.generateNextTwoPieces()
        self.gameStatus = 'running'
        self.gamePause = False

        self.bomb_available = self.bomb_unlocked
        self.bomb_queued = False

        # self.score = 0
        # self.level = STARTING_LEVEL
        self.lines = 0

        gameClock.restart(self.level)

    def erase_BLOCK(self, xRef, yRef, row, col):
        pygame.draw.rect(gameDisplay, BLACK,
                         [xRef + (col * self.blockSize), yRef + (row * self.blockSize), self.blockSize, self.blockSize],
                         0)

    def draw_BLOCK(self, xRef, yRef, row, col, color):
        pygame.draw.rect(gameDisplay, BLACK,
                         [xRef + (col * self.blockSize), yRef + (row * self.blockSize), self.blockSize,
                          self.blockLineWidth], 0)
        pygame.draw.rect(gameDisplay, BLACK, [xRef + (col * self.blockSize) + self.blockSize - self.blockLineWidth,
                                              yRef + (row * self.blockSize), self.blockLineWidth, self.blockSize], 0)
        pygame.draw.rect(gameDisplay, BLACK,
                         [xRef + (col * self.blockSize), yRef + (row * self.blockSize), self.blockLineWidth,
                          self.blockSize], 0)
        pygame.draw.rect(gameDisplay, BLACK, [xRef + (col * self.blockSize),
                                              yRef + (row * self.blockSize) + self.blockSize - self.blockLineWidth,
                                              self.blockSize, self.blockLineWidth], 0)

        pygame.draw.rect(gameDisplay, color, [xRef + (col * self.blockSize) + self.blockLineWidth,
                                              yRef + (row * self.blockSize) + self.blockLineWidth,
                                              self.blockSize - (2 * self.blockLineWidth),
                                              self.blockSize - (2 * self.blockLineWidth)], 0)

    def draw_GAMEBOARD_BORDER(self):
        # Draw the border
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos - self.boardLineWidth - self.blockLineWidth,
                                                     self.yPos - self.boardLineWidth - self.blockLineWidth,
                                                     (self.blockSize * self.colNum) + (2 * self.boardLineWidth) + (
                                                             2 * self.blockLineWidth), self.boardLineWidth], 0)
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos + (self.blockSize * self.colNum) + self.blockLineWidth,
                                                     self.yPos - self.boardLineWidth - self.blockLineWidth,
                                                     self.boardLineWidth,
                                                     (self.blockSize * self.rowNum) + (2 * self.boardLineWidth) + (
                                                             2 * self.blockLineWidth)], 0)
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos - self.boardLineWidth - self.blockLineWidth,
                                                     self.yPos - self.boardLineWidth - self.blockLineWidth,
                                                     self.boardLineWidth,
                                                     (self.blockSize * self.rowNum) + (2 * self.boardLineWidth) + (
                                                             2 * self.blockLineWidth)], 0)
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos - self.boardLineWidth - self.blockLineWidth,
                                                     self.yPos + (self.blockSize * self.rowNum) + self.blockLineWidth,
                                                     (self.blockSize * self.colNum) + (2 * self.boardLineWidth) + (
                                                             2 * self.blockLineWidth), self.boardLineWidth], 0)

        # Draw the grid
        for row in range(self.rowNum + 1):
            pygame.draw.line(gameDisplay, GRAY,
                             (self.xPos, self.yPos + row * self.blockSize),
                             (self.xPos + self.colNum * self.blockSize, self.yPos + row * self.blockSize), 1)

        for col in range(self.colNum + 1):
            pygame.draw.line(gameDisplay, GRAY,
                             (self.xPos + col * self.blockSize, self.yPos),
                             (self.xPos + col * self.blockSize, self.yPos + self.rowNum * self.blockSize), 1)

    def draw_GAMEBOARD_CONTENT(self):
        if self.gameStatus == 'firstStart':
            # Display title and version
            titleText = fontTitle.render('TETRIS', False, WHITE)
            gameDisplay.blit(titleText, (self.xPos + 1.55 * self.blockSize, self.yPos + 8 * self.blockSize))

            versionText = fontVersion.render('v 1.0', False, WHITE)
            gameDisplay.blit(versionText, (self.xPos + 7.2 * self.blockSize, self.yPos + 11.5 * self.blockSize))
        else:
            # Draw game board content
            for row in range(self.rowNum):
                for col in range(self.colNum):
                    if self.blockMat[row][col] == 'empty':
                        self.erase_BLOCK(self.xPos, self.yPos, row, col)
                    else:
                        self.draw_BLOCK(self.xPos, self.yPos, row, col, blockColors[self.blockMat[row][col]])

            # Draw moving piece and ghost positions
            if self.piece.status == 'moving':
                if self.ghost_block:
                    ghostPositions = self.piece.calculateGhostPosition()
                    for i in range(4):
                        self.draw_BLOCK(self.xPos, self.yPos, ghostPositions[i], self.piece.blocks[i].currentPos.col,
                                        LIGHT_GRAY)
                for i in range(4):
                    color = blockColors.get(self.piece.type, WHITE)
                    if self.piece.type == BOMB_PIECE_NAME:
                        color = self.redBlinkAnimation()
                    self.draw_BLOCK(
                        self.xPos,
                        self.yPos,
                        self.piece.blocks[i].currentPos.row,
                        self.piece.blocks[i].currentPos.col,
                        color,
                    )

            # Draw grid lines
            for row in range(self.rowNum + 1):
                pygame.draw.line(gameDisplay, GRAY,
                                 (self.xPos, self.yPos + row * self.blockSize),
                                 (self.xPos + self.colNum * self.blockSize, self.yPos + row * self.blockSize), 1)

            for col in range(self.colNum + 1):
                pygame.draw.line(gameDisplay, GRAY,
                                 (self.xPos + col * self.blockSize, self.yPos),
                                 (self.xPos + col * self.blockSize, self.yPos + self.rowNum * self.blockSize), 1)

            # Draw pause screen
            if self.gamePause:
                pygame.draw.rect(gameDisplay, DARK_GRAY,
                                 [self.xPos + self.blockSize, self.yPos + 8 * self.blockSize, 8 * self.blockSize,
                                  4 * self.blockSize], 0)
                pauseText = fontPAUSE.render('PAUSE', False, BLACK)
                gameDisplay.blit(pauseText, (self.xPos + 1.65 * self.blockSize, self.yPos + 8 * self.blockSize))

            # Draw game over screen
            if self.gameStatus == 'gameOver':
                pygame.draw.rect(gameDisplay, LIGHT_GRAY,
                                 [self.xPos + self.blockSize, self.yPos + 8 * self.blockSize, 8 * self.blockSize,
                                  8 * self.blockSize], 0)
                gameOverText0 = fontGAMEOVER.render('GAME', False, BLACK)
                gameDisplay.blit(gameOverText0, (self.xPos + 2.2 * self.blockSize, self.yPos + 8 * self.blockSize))
                gameOverText1 = fontGAMEOVER.render('OVER', False, BLACK)
                gameDisplay.blit(gameOverText1, (self.xPos + 2.35 * self.blockSize, self.yPos + 12 * self.blockSize))
    def draw_SCOREBOARD_BORDER(self):
        # Pre-calculate positions
        xStart = self.xPos + (self.blockSize * self.colNum) + self.blockLineWidth
        yStart = self.yPos - self.boardLineWidth - self.blockLineWidth
        xEnd = xStart + self.scoreBoardWidth + self.boardLineWidth
        yEnd = self.yPos + (self.blockSize * self.rowNum) + self.blockLineWidth

        # Draw scoreboard border
        pygame.draw.rect(gameDisplay, BORDER_COLOR,
                         [xStart, yStart, self.scoreBoardWidth + self.boardLineWidth, self.boardLineWidth], 0)
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [xEnd, yStart, self.boardLineWidth, yEnd - yStart], 0)
        pygame.draw.rect(gameDisplay, BORDER_COLOR,
                         [xStart, yEnd, self.scoreBoardWidth + self.boardLineWidth, self.boardLineWidth], 0)

    def draw_SCOREBOARD_CONTENT(self):

        xPosRef = self.xPos + (self.blockSize * self.colNum) + self.boardLineWidth + self.blockLineWidth
        yPosRef = self.yPos
        yLastBlock = self.yPos + (self.blockSize * self.rowNum)

        # Highscores laden
        if self.gameStatus == 'gameOver' or self.gameStatus == 'firstStart' or True:
            verschiebung = 200
            highscoreText = fontSB.render('Highscores:', False, TEXT_COLOR)
            gameDisplay.blit(highscoreText, (xPosRef + verschiebung, yPosRef))

            # Get the top 5 scores
            top_scores = SCORES.nlargest(10, 'Score')
            # check if the player name exists in the scores
            player_in_top_10 = False
            if self.playerName in top_scores['Name'].values:
                player_in_top_10 = True
            if self.playerName in SCORES['Name'].values:
                top_scores = SCORES.nlargest(9, 'Score')
            # Render top 5 scores
            for i, (name, score, level) in enumerate(top_scores.itertuples(index=False, name=None)):
                if name == self.playerName:
                    scoreText = fontSB.render(f"{i + 1}. YOU: {score} (Level: {level})", False, ORANGE)
                else:
                    scoreText = fontSB.render(f"{i + 1}. {name}: {score} (Level: {level})", False, NUM_COLOR)
                gameDisplay.blit(scoreText, (xPosRef + verschiebung, yPosRef + (i + 1) * 2 * self.blockSize))

            # Render player's score if it exists
            player_row = SCORES[SCORES['Name'] == self.playerName]
            if not player_row.empty and not player_in_top_10:
                player_score = player_row.iloc[0]['Score']
                player_level = player_row.iloc[0]['Level']
                # find the position of the player of all the players according to the score
                player_position = SCORES[SCORES['Score'] >= player_score].shape[0]
                scoreText = fontSB.render(f"{player_position}. YOU: {player_score} (Level: {player_level})", False, ORANGE)
                gameDisplay.blit(scoreText, (xPosRef + verschiebung, yPosRef + 10 * 2 * self.blockSize))


        if self.gameStatus == 'running':
            nextPieceText = fontSB.render('next:', False, TEXT_COLOR)
            gameDisplay.blit(nextPieceText, (xPosRef + self.blockSize, self.yPos))

            blocks = [[0, 0], [0, 0], [0, 0], [0, 0]]
            origin = [0, 0]
            next_color = blockColors.get(self.nextPieces[1], WHITE)
            if self.nextPieces[1] == BOMB_PIECE_NAME:
                next_color = self.redBlinkAnimation()
            for i in range(0, 4):
                blocks[i][ROW] = origin[ROW] + pieceDefs[self.nextPieces[1]][i][ROW]
                blocks[i][COL] = origin[COL] + pieceDefs[self.nextPieces[1]][i][COL]

                if self.nextPieces[1] == 'O':
                    self.draw_BLOCK(
                        xPosRef + 0.5 * self.blockSize,
                        yPosRef + 2.25 * self.blockSize,
                        blocks[i][ROW],
                        blocks[i][COL],
                        next_color,
                    )
                elif self.nextPieces[1] == 'I':
                    self.draw_BLOCK(
                        xPosRef + 0.5 * self.blockSize,
                        yPosRef + 1.65 * self.blockSize,
                        blocks[i][ROW],
                        blocks[i][COL],
                        next_color,
                    )
                else:
                    self.draw_BLOCK(
                        xPosRef + 1 * self.blockSize,
                        yPosRef + 2.25 * self.blockSize,
                        blocks[i][ROW],
                        blocks[i][COL],
                        next_color,
                    )

            if self.gamePause == False:
                pauseText = fontSmall.render('P -> pause', False, WHITE)
                gameDisplay.blit(pauseText, (xPosRef + 1 * self.blockSize, yLastBlock - 15 * self.blockSize))
            else:
                unpauseText = fontSmall.render('P -> unpause', False, self.whiteSineAnimation())
                gameDisplay.blit(unpauseText, (xPosRef + 1 * self.blockSize, yLastBlock - 15 * self.blockSize))

            if self.bomb_unlocked:
                if self.piece.type == BOMB_PIECE_NAME:
                    bomb_text = 'Bombe aktiv!'
                    bomb_color = self.redBlinkAnimation()
                elif self.bomb_queued:
                    bomb_text = 'Bombe eingeplant'
                    bomb_color = self.redBlinkAnimation()
                elif self.bomb_available:
                    bomb_text = 'B -> Bombe bereit'
                    bomb_color = self.redBlinkAnimation()
                else:
                    bomb_text = 'Bombe verbraucht'
                    bomb_color = GRAY

                bombText = fontSmall.render(bomb_text, False, bomb_color)
                gameDisplay.blit(bombText, (xPosRef + 1 * self.blockSize, yLastBlock - 14 * self.blockSize))

        else:

            yBlockRef = 0.3
            text0 = fontSB.render('press', False, self.whiteSineAnimation())
            gameDisplay.blit(text0, (xPosRef + self.blockSize, self.yPos + yBlockRef * self.blockSize))
            text1 = fontSB.render('enter', False, self.whiteSineAnimation())
            gameDisplay.blit(text1, (xPosRef + self.blockSize, self.yPos + (yBlockRef + 1.5) * self.blockSize))
            text2 = fontSB.render('to', False, self.whiteSineAnimation())
            gameDisplay.blit(text2, (xPosRef + self.blockSize, self.yPos + (yBlockRef + 3) * self.blockSize))
            if self.gameStatus == 'firstStart':
                text3 = fontSB.render('start', False, self.whiteSineAnimation())
                gameDisplay.blit(text3, (xPosRef + self.blockSize, self.yPos + (yBlockRef + 4.5) * self.blockSize))
            else:
                text3 = fontSB.render('restart', False, self.whiteSineAnimation())
                gameDisplay.blit(text3, (xPosRef + self.blockSize, self.yPos + (yBlockRef + 4.5) * self.blockSize))

        pygame.draw.rect(gameDisplay, BORDER_COLOR,
                         [xPosRef, yLastBlock - 12.5 * self.blockSize, self.scoreBoardWidth, self.boardLineWidth], 0)
        # Draw the score content
        self.draw_score_content(xPosRef, yLastBlock)

    # All the screen drawings occurs in this function, called at each game loop iteration

    def draw_score_content(self, xPosRef, yLastBlock):
        fac = -8

        scoreText = fontSB.render('score:', False, TEXT_COLOR)
        gameDisplay.blit(scoreText, (xPosRef + self.blockSize + fac, yLastBlock - 12 * self.blockSize))
        scoreNumText = fontSB.render(str(self.score), False, NUM_COLOR)
        gameDisplay.blit(scoreNumText, (xPosRef + self.blockSize, yLastBlock - 10 * self.blockSize))

        levelText = fontSB.render('level:', False, TEXT_COLOR)
        gameDisplay.blit(levelText, (xPosRef + self.blockSize + fac, yLastBlock - 8 * self.blockSize))
        levelNumText = fontSB.render(str(self.level), False, NUM_COLOR)
        gameDisplay.blit(levelNumText, (xPosRef + self.blockSize, yLastBlock - 6 * self.blockSize))

        level_up_score = 0
        for i in range(0, self.level + 1):
            level_up_score += LEVEL_SCORE * (LEVEL_SCORE_MULTIPLIER ** i)
        level_up_score -= self.score
        linesText = fontSB.render('level Up:', False, TEXT_COLOR)
        gameDisplay.blit(linesText, (xPosRef + self.blockSize + fac, yLastBlock - 4 * self.blockSize))
        linesNumText = fontSB.render(str(int(level_up_score)), False, NUM_COLOR)
        gameDisplay.blit(linesNumText, (xPosRef + self.blockSize, yLastBlock - 2 * self.blockSize))
    def draw(self):

        self.draw_GAMEBOARD_BORDER()
        self.draw_SCOREBOARD_BORDER()

        self.draw_GAMEBOARD_CONTENT()
        self.draw_SCOREBOARD_CONTENT()

    def whiteSineAnimation(self):

        sine = math.floor(255 * math.fabs(math.sin(2 * math.pi * (gameClock.frameTick / (SINE_ANI_PERIOD * 2)))))
        # sine = 127 + math.floor(127 * math.sin(2*math.pi*(gameClock.frameTick/SINE_ANI_PERIOD)))
        sineEffect = [sine, sine, sine]
        return sineEffect

    def redBlinkAnimation(self):

        sine = math.floor(150 + 105 * math.fabs(math.sin(2 * math.pi * (gameClock.frameTick / (SINE_ANI_PERIOD)))))
        sine = max(0, min(255, sine))
        return (sine, 30, 30)

    def lineClearAnimation(self):

        clearAniStage = math.floor((gameClock.frameTick - gameClock.clearAniStart) / CLEAR_ANI_PERIOD)
        halfCol = math.floor(self.colNum / 2)
        if clearAniStage < halfCol:
            for i in range(0, 4):
                if self.clearedLines[i] >= 0:
                    self.blockMat[self.clearedLines[i]][(halfCol) + clearAniStage] = 'empty'
                    self.blockMat[self.clearedLines[i]][(halfCol - 1) - clearAniStage] = 'empty'
        else:
            self.lineClearStatus = 'cleared'

    def dropFreeBlocks(self):  # Drops down the floating blocks after line clears occur

        for cLIndex in range(0, 4):
            if self.clearedLines[cLIndex] >= 0:
                for rowIndex in range(self.clearedLines[cLIndex], 0, -1):
                    for colIndex in range(0, self.colNum):
                        self.blockMat[rowIndex + cLIndex][colIndex] = self.blockMat[rowIndex + cLIndex - 1][colIndex]

                for colIndex in range(0, self.colNum):
                    self.blockMat[0][colIndex] = 'empty'

    def getCompleteLines(self):  # Returns index list(length of 4) of cleared lines(-1 if not assigned as cleared line)

        clearedLines = [-1, -1, -1, -1]
        cLIndex = -1
        rowIndex = self.rowNum - 1

        while rowIndex >= 0:
            for colIndex in range(0, self.colNum):
                if self.blockMat[rowIndex][colIndex] == 'empty':
                    rowIndex = rowIndex - 1
                    break
                if colIndex == self.colNum - 1:
                    cLIndex = cLIndex + 1
                    clearedLines[cLIndex] = rowIndex
                    rowIndex = rowIndex - 1

        if cLIndex >= 0:
            gameClock.clearAniStart = gameClock.frameTick
            self.lineClearStatus = 'clearRunning'
        else:
            self.prepareNextSpawn()

        return clearedLines

    def handle_bomb_explosion(self):
        """Entfernt Blöcke rund um die Bombe und bereitet den nächsten Spawn vor."""
        for block in self.piece.blocks:
            row = block.currentPos.row
            col = block.currentPos.col
            for d_row in (-1, 0, 1):
                for d_col in (-1, 0, 1):
                    target_row = row + d_row
                    target_col = col + d_col
                    if 0 <= target_row < self.rowNum and 0 <= target_col < self.colNum:
                        self.blockMat[target_row][target_col] = 'empty'

        self.clearedLines = [-1, -1, -1, -1]
        self.bomb_queued = False
        self.piece.dropScore = 0
        self.prepareNextSpawn()

    def prepareNextSpawn(self):
        self.generateNextPiece()
        self.lineClearStatus = 'idle'
        self.piece.status = 'uncreated'

    def queue_bomb(self) -> bool:
        """Ersetzt den nächsten Stein durch eine Bombe, falls verfügbar."""
        if not self.bomb_unlocked or not self.bomb_available or self.bomb_queued:
            return False
        if self.piece.type == BOMB_PIECE_NAME or self.nextPieces[1] == BOMB_PIECE_NAME:
            return False

        self.nextPieces[1] = BOMB_PIECE_NAME
        self.bomb_available = False
        self.bomb_queued = True
        return True

    def generateNextTwoPieces(self):
        self.nextPieces[0] = pieceNames[rng.randint(0, 6)]
        self.nextPieces[1] = pieceNames[rng.randint(0, 6)]
        self.piece.type = self.nextPieces[0]

    def generateNextPiece(self):
        self.nextPieces[0] = self.nextPieces[1]
        self.nextPieces[1] = pieceNames[rng.randint(0, 6)]
        self.piece.type = self.nextPieces[0]
        if self.piece.type == BOMB_PIECE_NAME:
            self.bomb_queued = False

    def checkAndApplyGameOver(self):
        if self.piece.gameOverCondition == True:
            self.gameStatus = 'gameOver'
            for i in range(0, 4):
                if self.piece.blocks[i].currentPos.row >= 0 and self.piece.blocks[i].currentPos.col >= 0:
                    self.blockMat[self.piece.blocks[i].currentPos.row][
                        self.piece.blocks[i].currentPos.col] = self.piece.type

    def check_win(self, target_level):
        return self.level >= target_level

    def updateScores(self):

        clearedLinesNum = 0
        for i in range(0, 4):
            if self.clearedLines[i] > -1:
                clearedLinesNum = clearedLinesNum + 1

        multiplier = 1
        if self.upgrades_data:
            try:
                multiplier = self.upgrades_data.get("score_multiplier", 1)
            except AttributeError:
                multiplier = 1

        self.score = self.score + ((self.level + 1) * baseLinePoints[clearedLinesNum] + self.piece.dropScore) * multiplier
        if self.score > 999999:
            self.score = 999999
        self.lines = self.lines + clearedLinesNum
        level_up_score = 0
        for i in range(0, self.level + 1):
            level_up_score += LEVEL_SCORE * (LEVEL_SCORE_MULTIPLIER ** i)
        while self.score > level_up_score:
            self.level = self.level + 1
            level_up_score += LEVEL_SCORE * (LEVEL_SCORE_MULTIPLIER ** self.level)
        if self.level > 99:
            self.level = 99

    def updateSpeed(self):
        """
        Aktualisiert die Fallgeschwindigkeit des Spielsteins basierend auf dem Level
        und berücksichtigt das Upgrade 'smoother_gravity' (verlangsamt Schwerkraft).
        """
        base_speed = STARTING_SPEED * (SPEED_MULTIPLIER ** self.level)
        if hasattr(self, "upgrades_data") and self.upgrades_data:
            try:
                upgrade_level = int(self.upgrades_data.get("unlocked", {}).get("smoother_gravity", 0))
            except Exception:
                upgrade_level = 0
            if upgrade_level > 0:
                base_speed *= (1.0 + 0.1 * upgrade_level - 0.05 * self.upgrades_data["smoother_gravity"])
        gameClock.fall = gameClock.TimingType(base_speed)

    def get_upgrade_level(self, key: str) -> int:
        """
        Liefert die Stufe des Upgrades `key` aus dem gespeicherten Upgrade-Dictionary.
        """
        if not hasattr(self, "upgrades_data") or not self.upgrades_data:
            return 0
        try:
            return int(self.upgrades_data.get("unlocked", {}).get(key, 0))
        except Exception:
            return 0

    def saveHighscore(self):
        # die zeile von dem player finden, falls es sie schon gibt
        player_row = SCORES[SCORES['Name'] == self.playerName]
        if not player_row.empty:
            # Update the existing player's score if it's higher
            if self.score > player_row.iloc[0]['Score']:
                SCORES.at[player_row.index[0], 'Score'] = self.score
            if self.level > player_row.iloc[0]['Level']:
                SCORES.at[player_row.index[0], 'Level'] = self.level

        else:
            # Add a new player if the name does not exist
            SCORES.loc[len(SCORES)] = [self.playerName, self.score, self.level]

    # All the game events and mechanics are placed in this function, called at each game loop iteration
    def gameAction(self):

        if self.gameStatus == 'firstStart':
            if key.enter.status == 'pressed':
                self.restart()

        elif self.gameStatus == 'gameOver':
            self.saveHighscore()
            # Check for player input to restart the game
            if key.enter.status == 'pressed':
                self.restart()


        elif self.gameStatus == 'running':

            #if key.restart.trig == True:
            #    self.restart()
            #    key.restart.trig = False

            if self.gamePause == False:

                self.piece.move(self.blockMat)
                self.checkAndApplyGameOver()

                if key.pause.trig == True:
                    gameClock.pause()
                    self.gamePause = True
                    key.pause.trig = False

                if self.gameStatus != 'gameOver':
                    if key.bomb.trig:
                        self.queue_bomb()
                        key.bomb.trig = False

                    if self.piece.status == 'moving':
                        self.rotate_CC()
                        self.rotate_cCC()

                        if key.cRotate.trig == True:
                            self.piece.rotate('cCW')
                            key.cRotate.trig = False

                        if key.hardDrop.trig == True and bool(self.upgrades_data.get("hard_drop", 0)):
                            self.perform_hard_drop()
                            key.hardDrop.trig = False

                    elif self.piece.status == 'collided':
                        if self.lineClearStatus == 'idle':
                            if self.piece.type == BOMB_PIECE_NAME:
                                self.handle_bomb_explosion()
                            else:
                                for i in range(0, 4):
                                    self.blockMat[self.piece.blocks[i].currentPos.row][
                                        self.piece.blocks[i].currentPos.col] = self.piece.type
                                self.clearedLines = self.getCompleteLines()
                                self.updateScores()
                                self.saveHighscore()
                                self.updateSpeed()
                        elif self.lineClearStatus == 'clearRunning':
                            self.lineClearAnimation()
                        else:  # 'clearFin'
                            self.dropFreeBlocks()
                            self.prepareNextSpawn()

            else:  # self.gamePause = False
                if key.pause.trig == True:
                    gameClock.unpause()
                    self.gamePause = False
                    key.pause.trig = False
                if key.bomb.trig:
                    key.bomb.trig = False

        else:  # 'gameOver'
            if key.enter.status == 'pressed':
                # self.restart()
                return

    def rotate_CC(self):
        if key.rotate.trig == True:
            self.rotate('CW')
            key.rotate.trig = False

    def rotate(self, direction):
        self.piece.rotate(direction)

    def rotate_cCC(self):
        if key.cRotate.trig == True:
            self.rotate('cCW')
            key.cRotate.trig = False

    def check_game_over(self):
        if self.gameStatus == 'gameOver' and key.enter.status == 'pressed':
            return True
        return False
