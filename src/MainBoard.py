from __future__ import annotations

import math

import pygame.mixer_music

from MovingPiece import MovingPiece
from config import *
from shared import gameClock, gameDisplay, key, rng, SCORES, line_clear_sound, tetris_sound, level_up_sound, bomb_sound, \
    piece_landed_sound


class MainBoard:

    SCORE_PANEL_BLOCKS = 10

    def __init__(self, starting_level, score=0, upgrades: dict | None = None):

        # Size and position initiations
        self.gameOver_accepted = False
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
        self.nextPieces: list[str] = []

        self.score = int(score)
        self.level = starting_level
        self.lines = 0
        self.num_pieces = 0

        self.playerName = ""
        self.inputActive = False

        self.upgrades_data: dict = upgrades or {}
        self._ensure_upgrade_defaults()

        self.ghost_block = bool(self.upgrades_data.get("ghost_piece", 0))

        # Upgrade-abhängige Features
        self.preview_extra = max(0, self.get_upgrade_level("preview_plus"))
        self.preview_count = 1 + self.preview_extra
        self.hold_unlocked = bool(self.get_upgrade_level("hold_unlocked"))
        self.hold_piece: str | None = None
        self.hold_used_this_piece = False

        self.updateSpeed()
        self.relapse_keys()
        self.updateSpeed()

    def perform_hard_drop(self):
        if self.piece.status != 'moving':
            return
        try:
            ghost_rows = self.piece.calculateGhostPosition()
            for i in range(4):
                # nur die Zeile auf die Ghost-Zeile setzen; Spalte bleibt
                self.piece.blocks[i].currentPos.row = ghost_rows[i]
            self.piece.status = 'collided'
        except Exception:
            # Falls irgendwas schiefgeh
            pass

    def relapse_keys(self):
        # Bewegungen
        key.down.trig = False
        key.down.status = 'idle'

        key.xNav.status = 'idle'  # links/rechts Navigation

        # Rotationen
        key.cRotate.trig = False
        key.cRotate.status = 'idle'

        key.rotate.trig = False
        key.rotate.status = 'idle'

        # Spezialaktionen
        key.bomb.trig = False
        key.bomb.status = 'idle'

        key.hardDrop.trig = False
        key.hardDrop.status = 'idle'

        if hasattr(key, "hold"):
            key.hold.trig = False
            key.hold.status = 'idle'

        # Sonstiges
        key.pause.trig = False
        key.pause.status = 'idle'

        key.restart.trig = False
        key.restart.status = 'idle'

        key.enter.trig = False
        key.enter.status = 'idle'

    def _ensure_upgrade_defaults(self) -> None:
        if self.upgrades_data is None:
            self.upgrades_data = {}

        unlocked_defaults = {
            "rotation_buffer": 0,
            "ghost_piece": 0,
            "smoother_gravity": 0,
            "score_multiplier": 1,
            "hard_drop": 0,
            "preview_plus": 0,
            "hold_unlocked": 0,
        }

        unlocked = self.upgrades_data.setdefault("unlocked", {})
        for key_name, default_value in unlocked_defaults.items():
            raw_value = unlocked.get(key_name, self.upgrades_data.get(key_name, default_value))
            try:
                value = int(raw_value)
            except Exception:
                value = default_value
            unlocked[key_name] = value
            self.upgrades_data.setdefault(key_name, value)

        try:
            meta_currency = int(self.upgrades_data.get("meta_currency", 0))
        except Exception:
            meta_currency = 0
        self.upgrades_data["meta_currency"] = meta_currency

    def setPlayerName(self, name):
        self.playerName = name
    def restart(self):
        self.blockMat = [['empty'] * self.colNum for i in range(self.rowNum)]

        self.lineClearStatus = 'idle'
        self.clearedLines = [-1, -1, -1, -1]
        gameClock.fall.preFrame = gameClock.frameTick
        self._ensure_upgrade_defaults()

        self.preview_extra = max(0, self.get_upgrade_level("preview_plus"))
        self.preview_count = max(1, 1 + self.preview_extra)
        self.hold_unlocked = bool(self.get_upgrade_level("hold_unlocked"))
        self.ghost_block = bool(self.get_upgrade_level("ghost_piece") or self.upgrades_data.get("ghost_piece", 0))

        self.hold_piece = None
        self.hold_used_this_piece = False
        self.num_pieces = 0

        self.nextPieces.clear()
        self.refill_next_queue()
        self.spawn_piece_from_queue()

        self.gameStatus = 'running'
        self.gamePause = False

        self.bomb_available = self.upgrades_data.get("bomb_block", 0) > 0
        self.bomb_queued = False

        # self.score = 0
        # self.level = STARTING_LEVEL
        self.lines = 0

        gameClock.restart(self.level)
        self.updateSpeed()

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

    def _score_panel_height(self) -> int:
        return int(self.blockSize * self.SCORE_PANEL_BLOCKS)

    def _score_panel_top(self, yLastBlock: int) -> int:
        return int(yLastBlock - self._score_panel_height())

    def _score_line_positions(self, yLastBlock: int, line_count: int) -> list[int]:
        panel_top = self._score_panel_top(yLastBlock)
        panel_height = self._score_panel_height()
        if line_count <= 1:
            return [panel_top + panel_height // 2]

        available_height = panel_height - self.blockSize
        spacing = available_height / (line_count - 1)
        start = panel_top + self.blockSize * 0.5
        return [int(start + spacing * i) for i in range(line_count)]

    def draw_SCOREBOARD_CONTENT(self):

        xPosRef = self.xPos + (self.blockSize * self.colNum) + self.boardLineWidth + self.blockLineWidth
        yPosRef = self.yPos
        yLastBlock = self.yPos + (self.blockSize * self.rowNum)
        score_panel_top = self._score_panel_top(yLastBlock)

        # Highscores laden (außerhalb des Scoreboards platziert)
        verschiebung = 200
        highscoreText = fontSB.render('Highscores:', False, TEXT_COLOR)
        gameDisplay.blit(highscoreText, (xPosRef + verschiebung, yPosRef))

        top_scores = SCORES.nlargest(10, 'Score')
        player_in_top_10 = self.playerName in top_scores['Name'].values
        if self.playerName in SCORES['Name'].values:
            top_scores = SCORES.nlargest(9, 'Score')

        for i, (name, score, level) in enumerate(top_scores.itertuples(index=False, name=None)):
            if name == self.playerName:
                scoreText = fontSB.render(f"{i + 1}. YOU: {score} (Level: {level})", False, ORANGE)
            else:
                scoreText = fontSB.render(f"{i + 1}. {name}: {score} (Level: {level})", False, NUM_COLOR)
            gameDisplay.blit(scoreText, (xPosRef + verschiebung, yPosRef + (i + 1) * 2 * self.blockSize))

        player_row = SCORES[SCORES['Name'] == self.playerName]
        if not player_row.empty and not player_in_top_10:
            player_score = player_row.iloc[0]['Score']
            player_level = player_row.iloc[0]['Level']
            player_position = SCORES[SCORES['Score'] >= player_score].shape[0]
            scoreText = fontSB.render(f"{player_position}. YOU: {player_score} (Level: {player_level})", False, ORANGE)
            gameDisplay.blit(scoreText, (xPosRef + verschiebung, yPosRef + 10 * 2 * self.blockSize))

        if self.gameStatus == 'running':
            self.draw_hold_and_next(xPosRef, yPosRef, score_panel_top)
            self.draw_pause_hint(xPosRef, score_panel_top)
        else:
            self.draw_start_prompt(xPosRef, yPosRef)

        pygame.draw.rect(gameDisplay, BORDER_COLOR,
                         [xPosRef, score_panel_top - self.boardLineWidth, self.scoreBoardWidth, self.boardLineWidth], 0)
        # Draw the score content
        self.draw_score_content(xPosRef, yLastBlock)

    def draw_hold_and_next(self, xPosRef: int, yPosRef: int, score_panel_top: int) -> None:
        available_height = score_panel_top - yPosRef
        if available_height <= 0:
            return

        # Upgrades können während der Kampagne freigeschaltet werden
        self.preview_extra = max(0, self.get_upgrade_level("preview_plus"))
        self.preview_count = max(1, 1 + self.preview_extra)
        self.hold_unlocked = bool(self.get_upgrade_level("hold_unlocked"))

        self.refill_next_queue()

        label_font = fontSmall
        label_height = label_font.get_height()
        top_margin = max(6, int(self.blockSize * 0.3))
        section_gap = max(6, int(self.blockSize * 0.2))
        preview_gap = max(4, int(self.blockSize * 0.1))

        hold_message_lines: list[str] = []

        message_height = 0
        if hold_message_lines:
            message_height = len(hold_message_lines) * label_height + (len(hold_message_lines) - 1) * 2

        box_count = self.preview_count + (1 if self.hold_unlocked else 0)
        total_label_height = label_height * 2
        total_gap = section_gap + preview_gap * max(0, self.preview_count)
        available_for_boxes = available_height - top_margin - total_label_height - total_gap - message_height
        if available_for_boxes <= 0:
            available_for_boxes = (self.preview_count) * 16

        block_size = 0
        if box_count > 0:
            block_size = available_for_boxes // (box_count * 4)
        block_size = max(3, min(self.blockSize, block_size))
        while block_size > 3 and block_size * 4 * box_count > available_for_boxes:
            block_size -= 1
        if block_size < 3:
            block_size = 3
        preview_box_size = block_size * 4

        center_x = int(xPosRef + self.scoreBoardWidth / 2)
        current_y = yPosRef + top_margin

        hold_label = label_font.render('HOLD', False, TEXT_COLOR)
        hold_label_rect = hold_label.get_rect()
        hold_rect = pygame.Rect(0, 0, preview_box_size, preview_box_size)

        if self.hold_unlocked:
            hold_label_rect.centerx = center_x
            hold_label_rect.top = current_y
            gameDisplay.blit(hold_label, hold_label_rect)

            current_y = hold_label_rect.bottom + 2

            hold_rect.centerx = center_x
            hold_rect.top = current_y
            pygame.draw.rect(gameDisplay, BORDER_COLOR, hold_rect, 1)

            inner_hold = hold_rect.inflate(-2, -2)
            if inner_hold.width <= 0 or inner_hold.height <= 0:
                inner_hold = hold_rect.copy()

        if not self.hold_unlocked:
            test = 0
        else:
            pygame.draw.rect(gameDisplay, BLACK, inner_hold)
            if self.hold_piece is None:
                placeholder = label_font.render('—', False, TEXT_COLOR)
                placeholder_rect = placeholder.get_rect(center=inner_hold.center)
                gameDisplay.blit(placeholder, placeholder_rect)
            else:
                self.draw_piece_preview(self.hold_piece, inner_hold, block_size)

        current_y = hold_rect.bottom + 2

        for line in hold_message_lines:
            msg_surface = label_font.render(line, False, LIGHT_GRAY)
            msg_rect = msg_surface.get_rect()
            msg_rect.centerx = center_x
            msg_rect.top = current_y
            gameDisplay.blit(msg_surface, msg_rect)
            current_y = msg_rect.bottom + 2

        current_y += section_gap

        current_y = max(current_y, 84)

        next_label = label_font.render('NEXT', False, TEXT_COLOR)
        next_label_rect = next_label.get_rect()
        next_label_rect.centerx = center_x
        next_label_rect.top = current_y
        gameDisplay.blit(next_label, next_label_rect)

        current_y = next_label_rect.bottom + 2

        self.refill_next_queue()
        for piece_type in self.nextPieces[:self.preview_count + 1]:
            if self.hold_unlocked:
                size = preview_box_size * 0.9
            else:
                size = preview_box_size * 1.1
            preview_rect = pygame.Rect(0, 0, size, size)
            preview_rect.centerx = center_x
            preview_rect.top = current_y
            pygame.draw.rect(gameDisplay, BORDER_COLOR, preview_rect, 1)
            current_y = preview_rect.bottom + preview_gap

            inner_preview = preview_rect.inflate(-2, -2)
            if inner_preview.width <= 0 or inner_preview.height <= 0:
                inner_preview = preview_rect.copy()
            pygame.draw.rect(gameDisplay, BLACK, inner_preview)

            if self.hold_unlocked:
                size = block_size * 0.9
            else:
                size = block_size

            self.draw_piece_preview(piece_type, inner_preview, size)
            if self.upgrades_data.get("bomb_block", 0) > 0:
                if self.piece.type == BOMB_PIECE_NAME:
                    bomb_text = 'Bombe aktiv!'
                    bomb_color = self.redBlinkAnimation()
                elif self.bomb_queued:
                    bomb_text = 'Bombe'
                    bomb_color = self.redBlinkAnimation()
                elif self.bomb_available:
                    bomb_text = f'B -> Bombe {int(self.upgrades_data.get("bomb_block", 0))}x'
                    bomb_color = self.redBlinkAnimation()
                else:
                    bomb_text = ''
                    bomb_color = GRAY

                bombText = fontSmall.render(bomb_text, False, bomb_color)
                gameDisplay.blit(bombText, (xPosRef + 1 * self.blockSize,  score_panel_top - fontSmall.get_height() + 300))

        else:

            current_y = preview_rect.bottom + preview_gap

    def draw_start_prompt(self, xPosRef: int, yPosRef: int) -> None:
        yBlockRef = 0.3
        text0 = fontSB.render('press', False, self.whiteSineAnimation())
        gameDisplay.blit(text0, (xPosRef + self.blockSize, yPosRef + yBlockRef * self.blockSize))
        text1 = fontSB.render('enter', False, self.whiteSineAnimation())
        gameDisplay.blit(text1, (xPosRef + self.blockSize, yPosRef + (yBlockRef + 1.5) * self.blockSize))
        text2 = fontSB.render('to', False, self.whiteSineAnimation())
        gameDisplay.blit(text2, (xPosRef + self.blockSize, yPosRef + (yBlockRef + 3) * self.blockSize))
        if self.gameStatus == 'firstStart':
            text3 = fontSB.render('start', False, self.whiteSineAnimation())
        else:
            text3 = fontSB.render('restart', False, self.whiteSineAnimation())
        gameDisplay.blit(text3, (xPosRef + self.blockSize, yPosRef + (yBlockRef + 4.5) * self.blockSize))

        yLastBlock = self.yPos + (self.blockSize * self.rowNum)
        score_panel_top = self._score_panel_top(yLastBlock)
        hint_y = score_panel_top - fontSmall.get_height() + 260
        pos_y_hard_drop = hint_y + 13
        # hint_y = max(hint_y, self.yPos)
        hint_x = self.blockSize + 50

        if self.upgrades_data.get("hard_drop", 0) > 0:
            if self.piece.status == 'moving':
                hard_drop_color = WHITE
            else:
                hard_drop_color = GRAY
            hard_drop_surface = fontSmall.render('SPACE -> hard drop', False, hard_drop_color)
            gameDisplay.blit(hard_drop_surface, (hint_x + 228, pos_y_hard_drop))

        # draw also the controls here
        controls_y = hint_y + 13
        controls = [
            ('Left/Right', 'move'),
            ('Down', 'faster drop'),
            ('Up', 'rotate'),
            ('Shift', 'rotate counter'),
        ]
        for i, (key_name, action) in enumerate(controls):
            control_surface = fontSmall.render(f'{key_name} -> {action}', False, WHITE)
            gameDisplay.blit(control_surface, (hint_x, controls_y + i * 13))

        # draw score muliplier if > 1
        font_big = pygame.font.SysFont('Arial', 12, bold=True)
        top = score_panel_top - fontSmall.get_height() + 230
        score_multiplier = self.upgrades_data.get("score_multiplier", 1)
        if score_multiplier > 1:
            multiplier_surface = font_big.render(f'Score x{round(score_multiplier, 1)}', False, ORANGE)
            gameDisplay.blit(multiplier_surface, (hint_x, top))

        # the same for smoother gravity
        smoother_gravity = self.get_upgrade_level("smoother_gravity")
        if smoother_gravity > 0:
            gravity_surface = font_big.render(f'Smoother Gravity Lv. {int(smoother_gravity / 4)}', False, ORANGE)
            gameDisplay.blit(gravity_surface, (hint_x + 200, top))

    def draw_pause_hint(self, xPosRef: int, score_panel_top: int) -> None:
        hint_y = score_panel_top - fontSmall.get_height() + 260
        pos_y_hard_drop = hint_y + 13
        #hint_y = max(hint_y, self.yPos)
        hint_x = self.blockSize + 50
        if self.gamePause:
            hint_surface = fontSmall.render('P -> unpause', False, self.whiteSineAnimation())
        else:
            hint_surface = fontSmall.render('P -> pause', False, WHITE)
        gameDisplay.blit(hint_surface, (hint_x, hint_y))

        if self.upgrades_data.get("hard_drop", 0) > 0:
            if self.piece.status == 'moving':
                hard_drop_color = WHITE
            else:
                hard_drop_color = GRAY
            hard_drop_surface = fontSmall.render('SPACE -> hard drop', False, hard_drop_color)
            gameDisplay.blit(hard_drop_surface, (hint_x + 228, pos_y_hard_drop))

        # draw also the controls here
        controls_y = hint_y + 13
        controls = [
            ('Left/Right', 'move'),
            ('Down', 'faster drop'),
            ('Up', 'rotate'),
            ('Shift', 'rotate counter'),
        ]
        for i, (key_name, action) in enumerate(controls):
            control_surface = fontSmall.render(f'{key_name} -> {action}', False, WHITE)
            gameDisplay.blit(control_surface, (hint_x, controls_y + i * 13))

        # draw score muliplier if > 1
        font_big = pygame.font.SysFont('Arial', 12, bold=True)
        top = score_panel_top - fontSmall.get_height() + 230
        score_multiplier = self.upgrades_data.get("score_multiplier", 1)
        if score_multiplier > 1:
            multiplier_surface = font_big.render(f'Score x{round(score_multiplier, 1)}', False, ORANGE)
            gameDisplay.blit(multiplier_surface, (hint_x, top))

        # the same for smoother gravity
        smoother_gravity = self.get_upgrade_level("smoother_gravity")
        if smoother_gravity > 0:
            gravity_surface = font_big.render(f'Smoother Gravity Lv. {int(smoother_gravity/4)}', False, ORANGE)
            gameDisplay.blit(gravity_surface, (hint_x + 200, top))

    def draw_piece_preview(self, piece_type: str, target_rect: pygame.Rect, block_size: int) -> None:
        if block_size <= 0:
            return
        definition = pieceDefs.get(piece_type)
        if not definition:
            return

        rows = [coor[ROW] for coor in definition]
        cols = [coor[COL] for coor in definition]
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        piece_width = (max_col - min_col + 1) * block_size
        piece_height = (max_row - min_row + 1) * block_size
        offset_x = target_rect.x + (target_rect.width - piece_width) // 2
        offset_y = target_rect.y + (target_rect.height - piece_height) // 2

        color = blockColors.get(piece_type, WHITE)
        for row, col in definition:
            x = offset_x + (col - min_col) * block_size
            y = offset_y + (row - min_row) * block_size
            pygame.draw.rect(gameDisplay, color, (x, y, block_size, block_size))
            pygame.draw.rect(gameDisplay, BLACK, (x, y, block_size, block_size), 1)

    # All the screen drawings occurs in this function, called at each game loop iteration

    def draw_score_content(self, xPosRef, yLastBlock):
        fac = -8
        positions = self._score_line_positions(yLastBlock, 6)

        scoreText = fontSB.render('score:', False, TEXT_COLOR)
        gameDisplay.blit(scoreText, (xPosRef + self.blockSize + fac, positions[0]))
        scoreNumText = fontSB.render(str(int(self.score)), False, NUM_COLOR)
        gameDisplay.blit(scoreNumText, (xPosRef + self.blockSize, positions[1] - 10))

        levelText = fontSB.render('level:', False, TEXT_COLOR)
        gameDisplay.blit(levelText, (xPosRef + self.blockSize + fac, positions[2] - 10))
        levelNumText = fontSB.render(str(self.level), False, NUM_COLOR)
        gameDisplay.blit(levelNumText, (xPosRef + self.blockSize, positions[3] - 10))

        level_up_score = 0
        for i in range(0, self.level + 1):
            level_up_score += LEVEL_SCORE * (LEVEL_SCORE_MULTIPLIER ** i)
        level_up_score -= self.score
        linesText = fontSB.render('level Up:', False, TEXT_COLOR)
        gameDisplay.blit(linesText, (xPosRef + self.blockSize + fac, positions[4] - 10))
        linesNumText = fontSB.render(str(int(level_up_score)), False, NUM_COLOR)
        gameDisplay.blit(linesNumText, (xPosRef + self.blockSize, positions[5] - 10))
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
        # play the bomb sound effect
        try:
            bomb_sound.play()
        except Exception:
            pass
        for block in self.piece.blocks:
            row = block.currentPos.row
            col = block.currentPos.col
            radius = 2
            for d_row in (-radius, 0, radius):
                for d_col in (-radius, 0, radius):
                    target_row = row + d_row
                    target_col = col + d_col
                    if 0 <= target_row < self.rowNum and 0 <= target_col < self.colNum:
                        self.blockMat[target_row][target_col] = 'empty'

        self.clearedLines = [-1, -1, -1, -1]
        self.bomb_queued = False
        self.piece.dropScore = 0
        self.prepareNextSpawn()

    def prepareNextSpawn(self):
        self.spawn_piece_from_queue()
        self.lineClearStatus = 'idle'

    def refill_next_queue(self) -> None:
        target_length = self.preview_count
        while len(self.nextPieces) < target_length:
            self.nextPieces.append(pieceNames[rng.randint(0, 6)])

    def _set_current_piece(self, piece_type: str, *, from_hold: bool = False, reset_hold_flag: bool = True) -> None:
        self.piece = MovingPiece(self.colNum, self.rowNum, 'uncreated')
        self.piece.type = piece_type
        if reset_hold_flag:
            self.hold_used_this_piece = False
        self.num_pieces += 1
        self.on_piece_spawned(from_hold=from_hold)
    def queue_bomb(self) -> bool:
        """Ersetzt den nächsten Stein durch eine Bombe, falls verfügbar."""
        if self.upgrades_data.get("bomb_block", 0) == 0 or self.bomb_queued:
            return False
        if self.piece.type == BOMB_PIECE_NAME or self.nextPieces[0] == BOMB_PIECE_NAME:
            return False

        self.nextPieces[0] = BOMB_PIECE_NAME
        self.upgrades_data["bomb_block"] = max(0, self.upgrades_data.get("bomb_block", 1) - 1)
        self.bomb_queued = True
        self.draw_SCOREBOARD_CONTENT()
        return True

    def generateNextTwoPieces(self):
        self.nextPieces[0] = pieceNames[rng.randint(0, 6)]
        self.nextPieces[1] = pieceNames[rng.randint(0, 6)]
        self.piece.type = self.nextPieces[0]

    def spawn_piece_from_queue(self, *, reset_hold_flag: bool = True, from_hold: bool = False) -> None:
        self.refill_next_queue()
        if not self.nextPieces:
            return
        next_type = self.nextPieces.pop(0)
        self._set_current_piece(next_type, from_hold=from_hold, reset_hold_flag=reset_hold_flag)
        self.refill_next_queue()

    def perform_hold(self) -> None:
        if not self.hold_unlocked:
            self.hold_unlocked = bool(self.get_upgrade_level("hold_unlocked"))
            if not self.hold_unlocked:
                return
        if self.hold_used_this_piece or self.piece.status != 'moving':
            return

        current_type = self.piece.type
        if self.hold_piece is None:
            self.hold_piece = current_type
            self.spawn_piece_from_queue(reset_hold_flag=False, from_hold=True)
        else:
            swap_type = self.hold_piece
            self.hold_piece = current_type
            self._set_current_piece(swap_type, from_hold=True, reset_hold_flag=False)

        self.hold_used_this_piece = True
        self.piece.move(self.blockMat)

    def on_piece_spawned(self, from_hold: bool = False) -> None:
        """Hook für Subklassen, wenn ein neues Piece gespawnt wurde."""
        return
    def generateNextPiece(self):
        self.nextPieces[0] = self.nextPieces[1]
        self.nextPieces[1] = pieceNames[rng.randint(0, 6)]
        self.piece.type = self.nextPieces[0]
        if self.piece.type == BOMB_PIECE_NAME:
            self.bomb_queued = False

    def checkAndApplyGameOver(self):
        if self.piece.gameOverCondition == True:
            self.gameStatus = 'gameOver'
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music/stinger-2021-08-30_-_Boss_Time_-_www.FesliyanStudios.com.mp3")
            pygame.mixer.music.play()
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

        if clearedLinesNum > 0 and clearedLinesNum < 4:
            # play sound effect
            try:
                line_clear_sound.play()
            except Exception:
                pass
        elif clearedLinesNum == 4:
            try:
                # Pause the music if it's playing
                pygame.mixer.music.pause()
                tetris_sound.play()
                # Resume the music after the tetris sound finishes
                pygame.mixer.music.unpause()
            except Exception:
                pass

        multiplier = 1
        if self.upgrades_data:
            try:
                multiplier = self.upgrades_data.get("score_multiplier", 1)
            except AttributeError:
                multiplier = 1

        self.score = self.score + baseLinePoints[clearedLinesNum] * multiplier
        if self.score > 999999:
            self.score = 999999
        self.lines = self.lines + clearedLinesNum
        level_up_score = 0
        for i in range(0, self.level + 1):
            level_up_score += LEVEL_SCORE * (LEVEL_SCORE_MULTIPLIER ** i)
        while self.score > level_up_score:
            # play the level up sound
            try:
                # check if tetris_sound is still playing, if so, stop it first
                level_up_sound.play()
            except Exception:
                pass
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
                self.gameOver_accepted = True


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
                        if hasattr(key, "hold") and key.hold.trig:
                            self.perform_hold()
                            key.hold.trig = False
                        self.rotate_CC()
                        self.rotate_cCC()

                        if key.cRotate.trig == True:
                            self.piece.rotate('cCW')
                            key.cRotate.trig = False

                        if key.hardDrop.trig == True and bool(self.upgrades_data.get("hard_drop", 0)):
                            self.perform_hard_drop()
                            key.hardDrop.trig = False

                    elif self.piece.status == 'collided':
                        if hasattr(key, "hold") and key.hold.trig:
                            key.hold.trig = False
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
        if self.gameStatus == 'gameOver' and self.gameOver_accepted:
            return True
        return False
