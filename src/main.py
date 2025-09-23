# Tetris Game, written in Python 3.6.5
# Version: 1.0
# Date: 26.05.2018
import sys
from config import *
from challenge_explainations import *
from shared import gameDisplay, gameClock, key, SCORES
from MainBoard import MainBoard
from challenge_test import Challenge_No_Rows
from challenge_upside_down import Challenge_Upside_Down
from challenge_spin import Challenge_Spin
import os
import random
import pygame

from src.challenge_rotation_limit import Challenge_Rotation_Limit
from src.challenge_rising_flood import Challenge_Rising_Flood
from src.upgrades import load_upgrades, save_upgrades


def gameLoop(name, target_level, mainBoard):
    clock = pygame.time.Clock()
    mainBoard.setPlayerName(name)

    xChange = 0

    gameExit = False

    while not gameExit:  # Stay in this loop unless the game is quit

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Looks for quitting event in every iteration (Meaning closing the game window)
                gameExit = True

            if event.type == pygame.KEYDOWN:  # Keyboard keys press events
                if event.key == pygame.K_LEFT:
                    xChange += -1
                if event.key == pygame.K_RIGHT:
                    xChange += 1
                if event.key == pygame.K_DOWN:
                    key.down.status = 'pressed'
                if event.key == pygame.K_UP:
                    if key.rotate.status == 'idle':
                        key.rotate.trig = True
                        key.rotate.status = 'pressed'
                if event.key == pygame.K_LSHIFT:
                    if key.cRotate.status == 'idle':
                        key.cRotate.trig = True
                        key.cRotate.status = 'pressed'
                if event.key == pygame.K_p:
                    if key.pause.status == 'idle':
                        key.pause.trig = True
                        key.pause.status = 'pressed'
                if event.key == pygame.K_r:
                    if key.restart.status == 'idle':
                        key.restart.trig = True
                        key.restart.status = 'pressed'
                if event.key == pygame.K_RETURN:
                    key.enter.status = 'pressed'
                if event.key == pygame.K_SPACE:
                    if key.hardDrop.status == 'idle':
                        key.hardDrop.trig = True
                        key.hardDrop.status = 'pressed'
                if event.key == pygame.K_b:
                    if key.bomb.status == 'idle':
                        key.bomb.trig = True
                        key.bomb.status = 'pressed'
                if event.key == pygame.K_h:
                    if key.hold.status == 'idle':
                        key.hold.trig = True
                        key.hold.status = 'pressed'

            if event.type == pygame.KEYUP:  # Keyboard keys release events
                if event.key == pygame.K_LEFT:
                    xChange += 1
                if event.key == pygame.K_RIGHT:
                    xChange += -1
                if event.key == pygame.K_DOWN:
                    key.down.status = 'released'
                if event.key == pygame.K_UP:
                    key.rotate.status = 'idle'
                if event.key == pygame.K_LSHIFT:
                    key.cRotate.status = 'idle'
                if event.key == pygame.K_p:
                    key.pause.status = 'idle'
                if event.key == pygame.K_r:
                    key.restart.status = 'idle'
                if event.key == pygame.K_RETURN:
                    key.enter.status = 'idle'
                if event.key == pygame.K_SPACE:
                    key.hardDrop.status = 'idle'
                if event.key == pygame.K_b:
                    key.bomb.status = 'idle'
                if event.key == pygame.K_h:
                    key.hold.status = 'idle'

            if xChange > 0:
                key.xNav.status = 'right'
            elif xChange < 0:
                key.xNav.status = 'left'
            else:
                key.xNav.status = 'idle'

        gameDisplay.fill(BLACK)  # Whole screen is painted black in every iteration before any other drawings occur

        mainBoard.gameAction()  # Apply all the game actions here

        if mainBoard.check_win(target_level):
            print("max level_reached")
            return False

        if mainBoard.check_game_over():
            print("game over")
            return True
        mainBoard.draw()  # Draw the new board after game the new game actions
        gameClock.update()  # Increment the frame tick

        pygame.display.update()  # Pygame display update
        clock.tick(60)  # Pygame clock tick function(60 fps)


def startup_login_screen():
    # Initialize the screen
    gameDisplay.fill(BLACK)
    logo_font = pygame.font.Font(None, 100)
    input_font = pygame.font.Font(None, 50)
    text_font = pygame.font.Font(None, 74)

    # Render Tetris logo
    logo_text = logo_font.render('TETRIS', True, WHITE)
    logo_rect = logo_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 5))
    gameDisplay.blit(logo_text, logo_rect)

    # Render input prompt
    text = text_font.render('Enter your name:', True, WHITE)
    text_rect = text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 3))
    gameDisplay.blit(text, text_rect)
    pygame.display.flip()
    max_name_length = 10

    PLAYER_NAME = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Confirm name input
                    if PLAYER_NAME.strip():  # Ensure name is not empty
                        if check_existing_name(PLAYER_NAME):  # Check if name exists
                            if not confirm_existing_name(PLAYER_NAME):
                                PLAYER_NAME = ""  # Reset name if not confirmed
                                continue
                        return PLAYER_NAME
                elif event.key == pygame.K_BACKSPACE:  # Delete last character
                    PLAYER_NAME = PLAYER_NAME[:-1]
                else:
                    if len(PLAYER_NAME) < max_name_length:  # Limit name length
                        PLAYER_NAME += event.unicode
        # Update the screen with the entered name
        gameDisplay.fill(BLACK)
        gameDisplay.blit(logo_text, logo_rect)
        gameDisplay.blit(text, text_rect)
        input_text = input_font.render(PLAYER_NAME, True, WHITE)
        input_rect = input_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
        gameDisplay.blit(input_text, input_rect)
        pygame.display.flip()


def check_existing_name(name):
    """Check if the name exists in the highscore DataFrame."""
    return not SCORES[SCORES['Name'] == name].empty


def confirm_existing_name(name):
    """Prompt the user to confirm if they are the existing player."""
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)
    text_line1 = font.render(f"{name} already exists!", True, WHITE)
    text_line2 = font.render(f"Are you {name}? (Y/N)", True, WHITE)

    text_rect1 = text_line1.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 30))
    text_rect2 = text_line2.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 30))

    gameDisplay.blit(text_line1, text_rect1)
    gameDisplay.blit(text_line2, text_rect2)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # Confirm
                    return True
                if event.key == pygame.K_n:  # Deny
                    return False

def normal_game(target_level, current_board, name):
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music/2021-10-19_-_Funny_Bit_-_www.FesliyanStudios.com.mp3')
    pygame.mixer.music.play(-1)  # Loop the music indefinitely
    return gameLoop(name=name, target_level=target_level, mainBoard=current_board)

def challenge_setup(challenge_explanation):
    # load challenge music
    pygame.mixer.music.load('music/fast-2021-08-30_-_Boss_Time_-_www.FesliyanStudios.com.mp3')
    pygame.mixer.music.play(-1)  # Loop the music indefinitely
    challenge_explanation()
    # skip the music to 30 seconds
    pygame.mixer.music.set_pos(30)
def challenge_lv_5(target_level, current_board, upgrades_data, name, challenge_explanation, upgrade = None, upgrade_screen = None):
    # setup
    challenge_setup(challenge_explanation)
    if gameLoop(name=name, target_level=target_level, mainBoard=current_board):
        return True

    # laod the stinger
    pygame.mixer.music.load('music/stinger-2021-10-19_-_Funny_Bit_-_www.FesliyanStudios.com.mp3')
    pygame.mixer.music.play()  # Play the stinger once

    if upgrade:
        if upgrades_data.get(upgrade, 0) == 0:
            upgrade_screen()
            upgrades_data[upgrade] += 1
        else:
            if upgrades_data.get("bomb_unlocked", 0) != 0:
                upgrades_data["bomb_block"] += 3
                challenge_done_screen_bomb()
            else:
                challenge_done_screen()
    else:
        if upgrades_data.get("bomb_unlocked", 0) != 0:
            upgrades_data["bomb_block"] += 3
            challenge_done_screen_bomb()

    return False

def challenge_lv_10(target_level, current_board, upgrades_data, name, challenge_explanation, upgrade=None,upgrade_screen=None):
    # setup
    challenge_setup(challenge_explanation)
    if gameLoop(name=name, target_level=target_level, mainBoard=current_board):
        return True

    # laod the stinger
    pygame.mixer.music.load('music/stinger-2021-10-19_-_Funny_Bit_-_www.FesliyanStudios.com.mp3')
    pygame.mixer.music.play()  # Play the stinger once

    if upgrade:
        if upgrades_data.get(upgrade, 0) == 0:
            upgrade_screen()
            upgrades_data[upgrade] += 1
        else:
            # random upgrade for smother gravity or score multiplier
            if random.choice([True, False]):
                upgrades_data["smoother_gravity"] += 0.5
                challenge_done_screen_smooth_fall()
            else:
                upgrades_data["score_multiplier"] = upgrades_data.get("score_multiplier", 1) + 0.1
                challenge_done_screen_score()
    else:
        # random upgrade for smother gravity or score multiplier
        if random.choice([True, False]):
            upgrades_data["smoother_gravity"] += 0.5
            challenge_done_screen_smooth_fall()
        else:
            upgrades_data["score_multiplier"] = upgrades_data.get("score_multiplier", 1) + 0.1
            challenge_done_screen_score()

    return False


def challenge_lv_25(target_level, current_board, upgrades_data, name, challenge_explanation, upgrade=None,upgrade_screen=None):
    # setup
    challenge_setup(challenge_explanation)
    if gameLoop(name=name, target_level=target_level, mainBoard=current_board):
        return True

    # laod the stinger
    pygame.mixer.music.load('music/stinger-2021-10-19_-_Funny_Bit_-_www.FesliyanStudios.com.mp3')
    pygame.mixer.music.play()  # Play the stinger once

    if upgrade:
        if upgrades_data.get(upgrade, 0) == 0:
            upgrade_screen()
            upgrades_data[upgrade] += 1
        else:
            # random upgrade for smother gravity or score multiplier
            if upgrades_data.get("preview_plus", 0) >= 3:
                upgrades_data["bomb_block"] += 3
                challenge_done_screen_bomb()
            else:
                upgrades_data["preview_plus"] += 1
                challenge_done_screen_preview()
    else:
        # random upgrade for smother gravity or score multiplier
        if upgrades_data.get("preview_plus", 0) >= 3:
            upgrades_data["bomb_block"] += 3
            challenge_done_screen_bomb()
        else:
            upgrades_data["preview_plus"] += 1
            challenge_done_screen_preview()

    return False

def calc_current_level(score, level_up_score=0):
    for i in range(0, 10000):
        level_up_score += LEVEL_SCORE * (LEVEL_SCORE_MULTIPLIER ** i)
        if level_up_score > score:
            return i


if __name__ == '__main__':
    try:
        pygame.display.set_caption('Tetris')
        name = startup_login_screen()
        #name = "robin"

        # Upgrades laden
        upgrades_data = load_upgrades(name)

        while True:
            current_board = MainBoard(STARTING_LEVEL, score= 0, upgrades=upgrades_data)
            if normal_game(target_level=5, current_board=current_board, name=name):
                continue

            current_board = Challenge_No_Rows(5, current_board.score, 20, upgrades=upgrades_data)
            if challenge_lv_5(target_level=6, current_board=current_board, upgrades_data=upgrades_data, name=name, challenge_explanation=challenge_explanation_screen_no_rows, upgrade="ghost_piece", upgrade_screen=challenge_done_screen_no_rows):
                continue

            if calc_current_level(current_board.score) < 10:
                current_board = MainBoard(calc_current_level(current_board.score), current_board.score, upgrades=upgrades_data)
                if normal_game(target_level=10, current_board=current_board, name=name):
                    continue
                # if the player has no bomb blocks, give them 3 for the challenge

                flood_interval = 12
                old_bomb = upgrades_data.get("bomb_block", 0)
                current_board = Challenge_Rising_Flood(calc_current_level(current_board.score), current_board.score,flood_interval_seconds=flood_interval,upgrades=upgrades_data)
                if challenge_lv_10(target_level=calc_current_level(current_board.score) + 1, current_board=current_board, upgrades_data=upgrades_data, name=name, challenge_explanation=lambda:challenge_explanation_screen_rising_flood(flood_interval), upgrade="hard_drop", upgrade_screen=None):
                    continue
                if old_bomb == 0 and upgrades_data.get("bomb_unlocked", 0) == 0:
                    upgrades_data["bomb_block"] = 3

            if calc_current_level(current_board.score) < 15:
                current_board = MainBoard(calc_current_level(current_board.score), current_board.score, upgrades=upgrades_data)
                if normal_game(target_level=15, current_board=current_board, name=name):
                    continue

                extra_rotation = upgrades_data.get("unlocked", {}).get("rotation_buffer", 0)
                current_board = Challenge_Rotation_Limit(calc_current_level(current_board.score), current_board.score, base_rotations=2, upgrades=upgrades_data)
                if challenge_lv_5(target_level=calc_current_level(current_board.score) + 1, current_board=current_board, upgrades_data=upgrades_data, name=name,
                                   challenge_explanation=lambda: challenge_explanation_screen_rotation_limit(2,
                                                                                                             extra_rotation),
                                   upgrade="rotation_buffer", upgrade_screen=challenge_done_screen_rotation_limit):
                    continue

            if calc_current_level(current_board.score) < 20:
                current_board = MainBoard(calc_current_level(current_board.score), current_board.score, upgrades=upgrades_data)
                if normal_game(target_level=20, current_board=current_board, name=name):
                    continue

                current_board = Challenge_Upside_Down(calc_current_level(current_board.score), current_board.score, upgrades=upgrades_data)
                if challenge_lv_10(target_level=calc_current_level(current_board.score) + 1, current_board=current_board, upgrades_data=upgrades_data, name=name,
                                  challenge_explanation=challenge_explanation_screen_upside_down, upgrade="hold_unlocked",
                                  upgrade_screen=challenge_done_screen_upside_down):
                    continue

            if calc_current_level(current_board.score) < 25:
                current_board = MainBoard(calc_current_level(current_board.score), current_board.score, upgrades=upgrades_data)
                if normal_game(target_level=25, current_board=current_board, name=name):
                    continue

                current_board = Challenge_Spin(calc_current_level(current_board.score), current_board.score, rotate_delay=15, upgrades=upgrades_data)
                if challenge_lv_25(target_level=calc_current_level(current_board.score) + 1, current_board=current_board, upgrades_data=upgrades_data, name=name,
                                    challenge_explanation=challenge_explanation_screen_spin, upgrade="preview_plus",
                                    upgrade_screen=None):
                        continue


            break
    except Exception as e:
        # Fehler-Handling
        print("An error occurred:", e)
        print("Exiting the game...")
    finally:
        # Highscores sichern und Spiel beenden
        # write the upgrades in the dataframe SCORES
        save_upgrades(name, upgrades_data)
        SCORES.to_csv(HIGHSCORES_FILE, index=False, header=True)
        pygame.quit()
        sys.exit()


