# Python
import sys


def challenge_explanation_screen_no_rows():
    # now a big text "upside down" in the middle of the screen upside down
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 100)
    text_surface = font.render("Reverse Tetris", True, WHITE)
    text_rect = text_surface.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
    gameDisplay.blit(text_surface, text_rect)

    # a text that explains the challenge below in one line
    font_small = pygame.font.Font(None, 40)
    explanation_text = font_small.render(f"Clear a line and you Loose", True,
                                         WHITE)
    explanation_rect = explanation_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 80))
    gameDisplay.blit(explanation_text, explanation_rect)

    # render prompt to continue
    font_small = pygame.font.Font(None, 30)
    continue_text = font_small.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 50))
    gameDisplay.blit(continue_text, continue_rect)
    pygame.display.flip()

    # wait for user to press enter
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# --- ROTATION LIMIT CHALLENGE SCREENS -----------------------------------------
import pygame
from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, BLACK, WHITE, fontTitle, fontSmall
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))

def _center(surface, y):
    rect = surface.get_rect(center=(DISPLAY_WIDTH // 2, y))
    gameDisplay.blit(surface, rect)

def challenge_explanation_screen_rotation_limit(base_rotations: int, extra_from_upgrades: int):
    # now a big text "upside down" in the middle of the screen upside down
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 100)
    text_surface = font.render("ROTATIONLIMIT", True, WHITE)
    text_rect = text_surface.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
    gameDisplay.blit(text_surface, text_rect)

    # a text that explains the challenge below in one line
    font_small = pygame.font.Font(None, 40)
    text_str = f"You can only rotate {base_rotations} times per piece" + (f" (+{extra_from_upgrades} from upgrades)" if extra_from_upgrades > 0 else "")
    explanation_text = font_small.render(text_str, True, WHITE)
    explanation_rect = explanation_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 80))
    gameDisplay.blit(explanation_text, explanation_rect)

    # render prompt to continue
    font_small = pygame.font.Font(None, 30)
    continue_text = font_small.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 50))
    gameDisplay.blit(continue_text, continue_rect)
    pygame.display.flip()

    # wait for user to press enter
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def challenge_done_screen_rotation_limit():
    # Clear the screen
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Render challenge completion message
    title_text = font.render("Challenge Completed!", True, WHITE)
    title_rect = title_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50))
    gameDisplay.blit(title_text, title_rect)

    # unlocked hold funktion with H key
    text = font.render("Your unlocked INSTANT-DROP with SPACE", True, WHITE)
    text_rect = text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 +25))
    gameDisplay.blit(text, text_rect)

    # Render prompt to continue
    font = pygame.font.Font(None, 30)
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 150))
    gameDisplay.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


def challenge_explanation_screen_rising_flood(interval_seconds: float) -> None:
    # now a big text "upside down" in the middle of the screen upside down
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 100)
    text_surface = font.render("GARBAGE FLOOD", True, WHITE)
    text_rect = text_surface.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
    gameDisplay.blit(text_surface, text_rect)

    # a text that explains the challenge below in one line
    font_small = pygame.font.Font(None, 40)
    explanation_text = font_small.render(f"Every {interval_seconds:.1f} seconds, a garbage row rises from below!", True, WHITE)
    explanation_rect = explanation_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 80))
    gameDisplay.blit(explanation_text, explanation_rect)

    # render prompt to continue
    font_small = pygame.font.Font(None, 30)
    continue_text = font_small.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 50))
    gameDisplay.blit(continue_text, continue_rect)
    pygame.display.flip()

    # wait for user to press enter
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


def challenge_done_screen_rising_flood() -> None:
    # Clear the screen
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Render challenge completion message
    title_text = font.render("Challenge Completed!", True, WHITE)
    title_rect = title_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50))
    gameDisplay.blit(title_text, title_rect)

    # unlocked hold funktion with H key
    text = font.render("Your unlocked BOMB-Feature and 3 BOMBS", True, WHITE)
    text_rect = text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 +25))
    gameDisplay.blit(text, text_rect)

    # Render prompt to continue
    font = pygame.font.Font(None, 30)
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 150))
    gameDisplay.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


def challenge_done_screen_bomb_unlock() -> None:
    """Screen shown when the bomb block upgrade is unlocked."""
    pygame.display.get_surface().fill(BLACK)

    title = fontTitle.render("Bombenblock freigeschaltet!", True, WHITE)
    _center(title, DISPLAY_HEIGHT // 2 - 40)

    hint_lines = [
        "Drücke B im Spiel, um den nächsten Stein durch eine Bombe zu ersetzen.",
        "Die Bombe blinkt rot und zerstört angrenzende Blöcke beim Aufprall.",
        "Bestätige mit ENTER, um weiterzuspielen.",
    ]

    y = DISPLAY_HEIGHT // 2 + 20
    for text in hint_lines:
        surface = fontSmall.render(text, True, WHITE)
        _center(surface, y)
        y += 35

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def challenge_done_screen():
    # Clear the screen
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Render challenge completion message
    title_text = font.render("Challenge Completed!", True, WHITE)
    title_rect = title_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50))
    gameDisplay.blit(title_text, title_rect)

    # Render prompt to continue
    font = pygame.font.Font(None, 30)
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 150))
    gameDisplay.blit(continue_text, continue_rect)

    pygame.display.flip()


def challenge_explanation_screen_upside_down():
    # now a big text "upside down" in the middle of the screen upside down
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 100)
    text_surface = font.render("UPSIDE DOWN", True, WHITE)
    text_surface = pygame.transform.rotate(text_surface, 180)
    text_rect = text_surface.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
    gameDisplay.blit(text_surface, text_rect)
    pygame.display.flip()

    # render prompt to continue
    font_small = pygame.font.Font(None, 30)
    continue_text = font_small.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 50))
    gameDisplay.blit(continue_text, continue_rect)
    pygame.display.flip()

    # wait for user to press enter
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def challenge_done_screen_upside_down():
    # Clear the screen
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Render challenge completion message
    title_text = font.render("Challenge Completed!", True, WHITE)
    title_rect = title_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50))
    gameDisplay.blit(title_text, title_rect)

    # unlocked hold funktion with H key
    text = font.render("You unlocked the Hold feature!", True, WHITE)
    text_rect = text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 +25))
    gameDisplay.blit(text, text_rect)

    # Render prompt to continue
    font = pygame.font.Font(None, 30)
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 150))
    gameDisplay.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


def challenge_done_screen_bomb():
    # Clear the screen
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Render challenge completion message
    title_text = font.render("Challenge Completed!", True, WHITE)
    title_rect = title_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50))
    gameDisplay.blit(title_text, title_rect)

    # unlocked hold funktion with H key
    text = font.render("You receive 3 BOMBS", True, WHITE)
    text_rect = text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 +25))
    gameDisplay.blit(text, text_rect)

    # Render prompt to continue
    font = pygame.font.Font(None, 30)
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 150))
    gameDisplay.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def challenge_done_screen_score():
    # Clear the screen
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Render challenge completion message
    title_text = font.render("Challenge Completed!", True, WHITE)
    title_rect = title_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50))
    gameDisplay.blit(title_text, title_rect)

    # unlocked hold funktion with H key
    text = font.render("Your Score multiplier increases", True, WHITE)
    text_rect = text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 +25))
    gameDisplay.blit(text, text_rect)

    # Render prompt to continue
    font = pygame.font.Font(None, 30)
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 150))
    gameDisplay.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def challenge_done_screen_smooth_fall():
    # Clear the screen
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Render challenge completion message
    title_text = font.render("Challenge Completed!", True, WHITE)
    title_rect = title_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50))
    gameDisplay.blit(title_text, title_rect)

    # unlocked hold funktion with H key
    text = font.render("Your Falling Speed decreases", True, WHITE)
    text_rect = text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 +25))
    gameDisplay.blit(text, text_rect)

    # Render prompt to continue
    font = pygame.font.Font(None, 30)
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 150))
    gameDisplay.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def challenge_done_screen_preview():
    # Clear the screen
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Render challenge completion message
    title_text = font.render("Challenge Completed!", True, WHITE)
    title_rect = title_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50))
    gameDisplay.blit(title_text, title_rect)

    # unlocked hold funktion with H key
    text = font.render("Your unlocked an extra preview space", True, WHITE)
    text_rect = text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 +25))
    gameDisplay.blit(text, text_rect)

    # Render prompt to continue
    font = pygame.font.Font(None, 30)
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 150))
    gameDisplay.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def challenge_done_screen_no_rows():
    # Clear the screen
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Render challenge completion message
    title_text = font.render("Challenge Completed!", True, WHITE)
    title_rect = title_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50))
    gameDisplay.blit(title_text, title_rect)

    # unlocked hold funktion with H key
    text = font.render("You unlocked the ghost piece feature", True, WHITE)
    text_rect = text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 +25))
    gameDisplay.blit(text, text_rect)

    # Render prompt to continue
    font = pygame.font.Font(None, 30)
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 150))
    gameDisplay.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def challenge_explanation_screen_spin():
    # now a big text "SPIN" in the middle of the screen that rotates slowly
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 100)
    angle = 0
    clock = pygame.time.Clock()
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

        gameDisplay.fill(BLACK)
        text_surface = font.render("SPIN", True, WHITE)
        rotated_surface = pygame.transform.rotate(text_surface, angle)
        text_rect = rotated_surface.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
        gameDisplay.blit(rotated_surface, text_rect)

        # render prompt to continue
        font_small = pygame.font.Font(None, 30)
        continue_text = font_small.render("Press ENTER to continue...", True, WHITE)
        continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 50))
        gameDisplay.blit(continue_text, continue_rect)

        pygame.display.flip()
        angle = (angle + 90) % 360
        clock.tick(3)


def main():
    # test all screens
    challenge_explanation_screen_no_rows()
    challenge_done_screen_no_rows()

    challenge_explanation_screen_rising_flood(10.0)
    challenge_done_screen_rising_flood()

    challenge_explanation_screen_rotation_limit(2, 1)
    challenge_explanation_screen_rotation_limit(2, 0)
    challenge_done_screen_rotation_limit()

    challenge_explanation_screen_upside_down()
    challenge_done_screen_upside_down()

    challenge_explanation_screen_spin()
    challenge_done_screen_preview()

    challenge_done_screen_smooth_fall()
    challenge_done_screen_score()
    challenge_done_screen_bomb()


if __name__ == "__main__":
    main()

