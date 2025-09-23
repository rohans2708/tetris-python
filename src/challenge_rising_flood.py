"""Challenge mode: Rising Flood (Garbage-Rush).

Periodically injects a garbage row from the bottom that pushes the field
upwards. A countdown shows when the next flood arrives and how many rows have
already risen. If the stack (or active piece) touches the top when the flood
hits, the game ends immediately.
"""

from __future__ import annotations

import math

from MainBoard import MainBoard
from src.config import fontSB, TEXT_COLOR, NUM_COLOR, LEVEL_SCORE, LEVEL_SCORE_MULTIPLIER
from src.shared import gameDisplay, rng


class Challenge_Rising_Flood(MainBoard):
    """MainBoard variant with periodic garbage rows rising from below."""

    _frames_per_second = 60

    def __init__(
        self,
        starting_level: int,
        score: int,
        flood_interval_seconds: float = 12.0,
        upgrades: dict | None = None,
    ) -> None:
        super().__init__(starting_level, score, upgrades)
        self.flood_interval_seconds = max(1.0, float(flood_interval_seconds))
        self.flood_interval_frames = max(
            1, int(self.flood_interval_seconds * self._frames_per_second)
        )
        self.frames_until_next_flood = self.flood_interval_frames
        self.flood_rows_added = 0

    # ------------------------------------------------------------------
    # Lifecycle helpers
    # ------------------------------------------------------------------

    def restart(self) -> None:
        super().restart()
        self.frames_until_next_flood = self.flood_interval_frames
        self.flood_rows_added = 0

    def gameAction(self) -> None:  # type: ignore[override]
        super().gameAction()
        if self.gameStatus == 'running' and not self.gamePause:
            self._update_flood_timer()

    # ------------------------------------------------------------------
    # Flood mechanics
    # ------------------------------------------------------------------

    def _update_flood_timer(self) -> None:
        if self.frames_until_next_flood > 0:
            self.frames_until_next_flood -= 1

        if self.frames_until_next_flood <= 0:
            flooded = self._trigger_flood()
            if self.gameStatus == 'gameOver':
                return
            if flooded:
                self.frames_until_next_flood = self.flood_interval_frames
            else:
                # try again shortly (e.g. while a line clear animation runs)
                self.frames_until_next_flood = 1

    def _trigger_flood(self) -> bool:
        # Avoid conflicting with the line clear animation – try again shortly.
        if self.lineClearStatus != 'idle':
            return False

        # If the top row already contains blocks, the rising flood ends the game.
        if any(cell != 'empty' for cell in self.blockMat[0]):
            self.gameStatus = 'gameOver'
            return False

        # Active piece reaches the ceiling – cannot raise the board safely.
        if self.piece.status == 'moving':
            if any(block.currentPos.row <= 0 for block in self.piece.blocks):
                self.gameStatus = 'gameOver'
                return False

        self._raise_board()
        return True

    def _raise_board(self) -> None:
        # Push the locked stack upwards by one row.
        for row in range(self.rowNum - 1):
            self.blockMat[row] = list(self.blockMat[row + 1])

        # Inject new garbage row with a random hole at the bottom.
        hole_col = rng.randint(0, self.colNum - 1)
        new_row = ['garbage'] * self.colNum
        new_row[hole_col] = 'empty'
        self.blockMat[self.rowNum - 1] = new_row

        self.flood_rows_added += 1

        # Move the active piece one row up to match the rising stack.
        if self.piece.status == 'moving':
            for block in self.piece.blocks:
                block.currentPos.row -= 1
                block.nextPos.row = block.currentPos.row

    # ------------------------------------------------------------------
    # Scoreboard overlay
    # ------------------------------------------------------------------

    def draw_score_content(self, xPosRef: int, yLastBlock: int) -> None:
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

        floodText = fontSB.render('flood:', False, TEXT_COLOR)
        gameDisplay.blit(floodText, (xPosRef + self.blockSize, positions[4]))
        seconds_left = max(
            0,
            math.ceil(self.frames_until_next_flood / self._frames_per_second),
        )
        floodValue = fontSB.render(f'{seconds_left}s', False, NUM_COLOR)
        gameDisplay.blit(floodValue, (xPosRef + self.blockSize, positions[5]))

        """
        level_up_score = 0
        for i in range(0, self.level + 1):
            level_up_score += LEVEL_SCORE * (LEVEL_SCORE_MULTIPLIER ** i)
        level_up_score -= self.score
        linesText = fontSB.render('level Up:', False, TEXT_COLOR)
        gameDisplay.blit(linesText, (xPosRef + self.blockSize, positions[6]))
        linesNumText = fontSB.render(str(int(level_up_score)), False, NUM_COLOR)
        gameDisplay.blit(linesNumText, (xPosRef + self.blockSize, positions[7]))
        """
