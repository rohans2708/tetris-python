from GameKeyInput import GameKeyInput
from GameClock import GameClock
import pygame
import random
from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, SEED, HIGHSCORES_FILE
import pandas as pd

pygame.init()
pygame.font.init()
pygame.mixer.init()

line_clear_sound = pygame.mixer.Sound("music/sfx28-attack-338386.mp3")
tetris_sound = pygame.mixer.Sound("music/victory-85561.mp3")
level_up_sound = pygame.mixer.Sound("music/8-bit-powerup-6768.mp3")
bomb_sound = pygame.mixer.Sound("music/8-bit-explosion-3-340456.mp3")
piece_landed_sound = pygame.mixer.Sound("music/retro-hurt-1-236672.mp3")
level_up_sound.set_volume(0.8)
#tetris_sound.set_volume(10)

#gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT), pygame.FULLSCREEN)
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
gameClock = GameClock()
key = GameKeyInput()

rng = random.Random(SEED)

SCORES = pd.read_csv(HIGHSCORES_FILE, skiprows=1, names=['Name', 'Score', 'Level'])

# Convert 'Score' column to numeric and drop invalid rows
SCORES['Score'] = pd.to_numeric(SCORES['Score'], errors='coerce').fillna(0).astype(int)
SCORES['Level'] = pd.to_numeric(SCORES['Level'], errors='coerce').fillna(0).astype(int)
SCORES = SCORES.dropna(subset=['Score'])
SCORES = SCORES.dropna(subset=['Level'])

PLAYER_NAME = ""

