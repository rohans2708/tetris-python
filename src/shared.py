from GameKeyInput import GameKeyInput
from GameClock import GameClock
import pygame
import random
from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, SEED, HIGHSCORES_FILE
import pandas as pd

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Load background music
pygame.mixer.music.load('music/2021-10-19_-_Funny_Bit_-_www.FesliyanStudios.com.mp3')

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT)) #, pygame.FULLSCREEN)
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

