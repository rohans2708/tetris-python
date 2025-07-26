# Python
import sys

import pygame

from config import *
from src.shared import gameDisplay


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