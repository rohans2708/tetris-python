from __future__ import annotations

from MainBoard import MainBoard
from src.config import fontSB, TEXT_COLOR, NUM_COLOR
from src.shared import gameDisplay


class Challenge_Rotation_Limit(MainBoard):

    def __init__(
        self,
        starting_level: int,
        score: int,
        base_rotations: int = 2,
        upgrades: dict | None = None,
    ) -> None:
        super().__init__(starting_level, score, upgrades)
        self.base_rotations = max(0, int(base_rotations))
        self.rotations_left: int = self.base_rotations

    # ---------- Rotations-Logik ----------

    def rotate(self, direction):
        if self.rotations_left > 0:
            super().rotate(direction)
            self.rotations_left -= 1

    # ---------- Scoreboard-Overlay ----------

    def draw_score_content(self, xPosRef: int, yLastBlock: int) -> None:
        positions = self._score_line_positions(yLastBlock, 6)
        # 10 Pixel nach oben verschieben
        positions = [pos - 10 for pos in positions]

        scoreText = fontSB.render('score:', False, TEXT_COLOR)
        gameDisplay.blit(scoreText, (xPosRef + self.blockSize, positions[0]))
        scoreNumText = fontSB.render(str(self.score), False, NUM_COLOR)
        gameDisplay.blit(scoreNumText, (xPosRef + self.blockSize, positions[1]))

        levelText = fontSB.render('level:', False, TEXT_COLOR)
        gameDisplay.blit(levelText, (xPosRef + self.blockSize, positions[2]))
        levelNumText = fontSB.render(str(self.level), False, NUM_COLOR)
        gameDisplay.blit(levelNumText, (xPosRef + self.blockSize, positions[3]))

        rotText = fontSB.render('rotations:', False, TEXT_COLOR)
        gameDisplay.blit(rotText, (xPosRef + self.blockSize, positions[4]))
        rotNumText = fontSB.render(str(max(0, self.rotations_left)), False, NUM_COLOR)
        gameDisplay.blit(rotNumText, (xPosRef + self.blockSize, positions[5]))

    def on_piece_spawned(self, from_hold: bool = False) -> None:
        self.rotations_left = self.base_rotations + max(0, self.get_upgrade_level("rotation_buffer"))
        super().on_piece_spawned(from_hold)
