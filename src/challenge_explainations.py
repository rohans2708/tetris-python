# Python
import sys

import pygame

from config import *
from shared import gameDisplay


def challenge_explanation_screen_no_rows():
    # Initialize the screen
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Render challenge explanation
    challenge_text = [
        "Challenge Explanation:",
        "1. Lose if a row is completely filled.",
        "2. Place 20 pieces to level up."
    ]

    for i, line in enumerate(challenge_text):
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 3 + i * 50))
        gameDisplay.blit(text_surface, text_rect)

    # Render prompt to continue
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 100))
    gameDisplay.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN:
                return

def challenge_done_screen_no_rows():
    # Initialize the screen
    gameDisplay.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Render challenge explanation
    challenge_text = [
        "Challenge Passed:",
        "You unlocked the ghost piece feature!",
    ]

    for i, line in enumerate(challenge_text):
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + i * 50))
        gameDisplay.blit(text_surface, text_rect)

    # Render prompt to continue
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 100))
    gameDisplay.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN:
                return

# --- ROTATION LIMIT CHALLENGE SCREENS -----------------------------------------
import pygame
from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, BLACK, WHITE, fontTitle, fontSmall
from shared import gameDisplay

def _center(surface, y):
    rect = surface.get_rect(center=(DISPLAY_WIDTH // 2, y))
    gameDisplay.blit(surface, rect)

def challenge_explanation_screen_rotation_limit(base_rotations: int, extra_from_upgrades: int):
    """
    Zeigt einen Erklär-Screen für die Rotationslimit-Challenge.
    base_rotations: Grundlimit pro Stein (z.B. 2)
    extra_from_upgrades: Bonus-Rotationen durch dauerhaftes Upgrade (z.B. rotation_buffer)
    """
    pygame.display.get_surface().fill(BLACK)

    title = fontTitle.render("Challenge: Rotationslimit", True, WHITE)
    _center(title, DISPLAY_HEIGHT // 5)

    # Textzeilen
    total = base_rotations + max(0, extra_from_upgrades)
    lines = [
        f"Jedes Piece darf nur {base_rotations} Rotationen ausführen.",
        f"Dauerhaftes Upgrade-Bonus: +{max(0, extra_from_upgrades)}",
        f"Effektiv: {total} Rotationen pro Piece.",
        "Unten rechts siehst du live, wie viele Rotationen übrig sind.",
        "Drücke ENTER, um zu starten.",
    ]

    y = DISPLAY_HEIGHT // 3
    for txt in lines:
        surf = fontSmall.render(txt, True, WHITE)
        _center(surf, y)
        y += 40

    pygame.display.flip()

    # warten bis ENTER
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def challenge_done_screen_rotation_limit():
    """Optionaler 'Geschafft!'-Screen nach der Challenge."""
    pygame.display.get_surface().fill(BLACK)

    title = fontTitle.render("Rotationslimit geschafft!", True, WHITE)
    _center(title, DISPLAY_HEIGHT // 2 - 30)

    hint = fontSmall.render("Drücke ENTER, um weiterzuspielen.", True, WHITE)
    _center(hint, DISPLAY_HEIGHT // 2 + 30)

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
    continue_text = font.render("Press ENTER to continue...", True, WHITE)
    continue_rect = continue_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 50))
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