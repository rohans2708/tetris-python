# Tetris Game, written in Python 3.6.5
# Version: 1.0
# Date: 26.05.2018
import sys
from config import *
from challenge_explainations import *
from shared import gameDisplay, gameClock, key, SCORES
from MainBoard import MainBoard
from challenge_test import Challenge_No_Rows
from challenge_spin import Challenge_Spin
import os

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
                if event.key == pygame.K_z:
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

            if event.type == pygame.KEYUP:  # Keyboard keys release events
                if event.key == pygame.K_LEFT:
                    xChange += 1
                if event.key == pygame.K_RIGHT:
                    xChange += -1
                if event.key == pygame.K_DOWN:
                    key.down.status = 'released'
                if event.key == pygame.K_UP:
                    key.rotate.status = 'idle'
                if event.key == pygame.K_z:
                    key.cRotate.status = 'idle'
                if event.key == pygame.K_p:
                    key.pause.status = 'idle'
                if event.key == pygame.K_r:
                    key.restart.status = 'idle'
                if event.key == pygame.K_RETURN:
                    key.enter.status = 'idle'

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


if __name__ == '__main__':

    try:
        pygame.display.set_caption('Tetris')

        name = startup_login_screen()
        current_board = MainBoard(STARTING_LEVEL)

        # upgrades
        ghost_block = False


        while True:
            if gameLoop(name=name, target_level=3, mainBoard=current_board):
                continue     # Start the game loop
            challenge_explanation_screen_no_rows()
            current_board = Challenge_No_Rows(4, current_board.score, 20)  # Initialize the challenge board
            if gameLoop(name=name, target_level=5, mainBoard=current_board):  # Start the challenge loop
                continue
            ghost_block = True
            challenge_done_screen_no_rows()

            current_board = MainBoard(5, current_board.score, ghost_block)  # Reset to main board after challenge
            if gameLoop(name=name, target_level=8, mainBoard=current_board):
                continue
            current_board = Challenge_Spin(8, current_board.score, rotate_delay=30, ghost_piece=ghost_block)
            if gameLoop(name=name, target_level=10, mainBoard=current_board):
                continue
            current_board = MainBoard(10, current_board.score, ghost_block)  # Reset to main board after challenge
            if gameLoop(name=name, target_level=50, mainBoard=current_board):
                continue
            break


    except Exception as e:
        print("An error occurred:", e)
        print("Exiting the game...")
    finally:
        # save the high scores to the CSV file before exiting
        SCORES.to_csv(HIGHSCORES_FILE, index=False, header=True)
        print("High scores saved to", HIGHSCORES_FILE)
        pygame.quit()
        sys.exit()


