"""
Rotation-Limit-Challenge für das Tetris-Spiel.

Jedes Piece darf nur eine begrenzte Anzahl Rotationen ausführen, bevor es
sperrt. Die Basiszahl an erlaubten Rotationen kann konfiguriert werden.
Über das dauerhafte Upgrade `rotation_buffer` erhält der Spieler weitere
Rotationen pro Stein. Nach dem Spawn eines neuen Steins wird der Zähler
neu gesetzt.
"""

from __future__ import annotations

from typing import Callable
from MainBoard import MainBoard
from src.config import fontSB, TEXT_COLOR, NUM_COLOR  # Fonts/Farben
from src.shared import gameDisplay, key  # Surface für Textausgabe


class Challenge_Rotation_Limit(MainBoard):
    """Challenge-Board: Limitiert Rotationen pro Stein und zeigt Rest an."""

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
        """Rotation nur erlauben, wenn noch welche übrig sind."""
        if self.rotations_left > 0:
            super().rotate(direction)
            self.rotations_left -= 1

    def prepareNextSpawn(self):
        self.rotations_left = self.base_rotations
        super().prepareNextSpawn()

    # ---------- Scoreboard-Overlay ----------

    def draw_score_content(self, xPosRef: int, yLastBlock: int) -> None:
        """
        Zusätzlicher Scoreboard-Block für diese Challenge.
        Zeigt Score/Level und die verbleibenden Rotationen an.
        (Layout analog zu Challenge_No_Rows gehalten.)
        """
        # Score
        scoreText = fontSB.render('score:', False, TEXT_COLOR)
        gameDisplay.blit(scoreText, (xPosRef + self.blockSize, yLastBlock - 12 * self.blockSize))
        scoreNumText = fontSB.render(str(self.score), False, NUM_COLOR)
        gameDisplay.blit(scoreNumText, (xPosRef + self.blockSize, yLastBlock - 10 * self.blockSize))

        # Level
        levelText = fontSB.render('level:', False, TEXT_COLOR)
        gameDisplay.blit(levelText, (xPosRef + self.blockSize, yLastBlock - 8 * self.blockSize))
        levelNumText = fontSB.render(str(self.level), False, NUM_COLOR)
        gameDisplay.blit(levelNumText, (xPosRef + self.blockSize, yLastBlock - 6 * self.blockSize))

        # Verbleibende Rotationen (live)
        rotText = fontSB.render('rotations:', False, TEXT_COLOR)
        gameDisplay.blit(rotText, (xPosRef + self.blockSize, yLastBlock - 4 * self.blockSize))
        rotNumText = fontSB.render(str(max(0, self.rotations_left)), False, NUM_COLOR)
        gameDisplay.blit(rotNumText, (xPosRef + self.blockSize, yLastBlock - 2 * self.blockSize))
