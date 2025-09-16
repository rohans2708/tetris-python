import pygame
import time

SEED = time.time_ns()  # Use current time in nanoseconds as a seed for randomness
HIGHSCORES_FILE = "scores.csv"

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

pieceNames = ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
# Special piece that can be triggered via upgrade (not part of normal random bag)
BOMB_PIECE_NAME = 'BOMB'

STARTING_SPEED = 48
SPEED_MULTIPLIER = 0.9

LEVEL_SCORE = 700
LEVEL_SCORE_MULTIPLIER = 1.1

STARTING_LEVEL = 0 #Change this to start a new game at a higher level

MOVE_PERIOD_INIT = 4 #Piece movement speed when up/right/left arrow keys are pressed (Speed is defined as frame count. Game is 60 fps)

CLEAR_ANI_PERIOD = 4 #Line clear animation speed
SINE_ANI_PERIOD = 120 #Sine blinking effect speed


ROW = (0)
COL = (1)

#Some color definitions
BLACK = (0,0,0)
WHITE = (255,255,255)
DARK_GRAY = (80,80,80)
GRAY = (110,110,110)
LIGHT_GRAY = (150,150,150)
ORANGE = (240,110,2)
BORDER_COLOR = GRAY
NUM_COLOR = WHITE
TEXT_COLOR = GRAY

blockColors = {
    'I': (19, 232, 232),  # CYAN
    'O': (236, 236, 14),  # YELLOW
    'T': (126, 5, 126),  # PURPLE
    'S': (0, 128, 0),  # GREEN
    'Z': (236, 14, 14),  # RED
    'J': (30, 30, 201),  # BLUE
    'L': (240, 110, 2),  # ORANGE
    BOMB_PIECE_NAME: (200, 30, 30),  # BASE COLOR FOR BOMB (BLINKS IN-GAME)
    'garbage': (90, 90, 90),
}

#Initial(spawn) block definitons of each piece
pieceDefs = {
'I' : ((1,0),(1,1),(1,2),(1,3)),
'O' : ((0,1),(0,2),(1,1),(1,2)),
'T' : ((0,1),(1,0),(1,1),(1,2)),
'S' : ((0,1),(0,2),(1,0),(1,1)),
'Z' : ((0,0),(0,1),(1,1),(1,2)),
'J' : ((0,0),(1,0),(1,1),(1,2)),
'L' : ((0,2),(1,0),(1,1),(1,2)),
BOMB_PIECE_NAME : ((0,1),(0,2),(1,1),(1,2)) }

directions = {
'down' : (1,0),
'right' : (0,1),
'left' : (0,-1),
'downRight' : (1,1),
'downLeft' : (1,-1),
'noMove' : (0,0) }

levelSpeeds = (48,43,38,33,28,23,18,13,8,6,5,5,5,4,4,4,3,3,3,2,2,2,2,2,2,2,2,2,2)
#The speed of the moving piece at each level. Level speeds are defined as levelSpeeds[level]
#Each 10 cleared lines means a level up.
#After level 29, speed is always 1. Max level is 99

baseLinePoints = (0,40,100,300,1200)
#Total score is calculated as: Score = level*baseLinePoints[clearedLineNumberAtATime] + totalDropCount
#Drop means the action the player forces the piece down instead of free fall(By key combinations: down, down-left, down-rigth arrows)

blockSize = 20
boardColNum = 10
boardRowNum = 20
boardLineWidth = 10
blockLineWidth = 1
scoreBoardWidth = blockSize * (boardColNum//2)
boardPosX = DISPLAY_WIDTH*0.1
boardPosY = DISPLAY_HEIGHT*0.15

# font
pygame.init()
pygame.font.init()

#Font sizes
SB_FONT_SIZE = 29
FONT_SIZE_SMALL = 17
PAUSE_FONT_SIZE = 66
GAMEOVER_FONT_SIZE = 66
TITLE_FONT_SIZE = 70
VERSION_FONT_SIZE = 20

fontSB = pygame.font.SysFont('agencyfb', SB_FONT_SIZE)
fontSmall = pygame.font.SysFont('agencyfb', FONT_SIZE_SMALL)
fontPAUSE = pygame.font.SysFont('agencyfb', PAUSE_FONT_SIZE)
fontGAMEOVER = pygame.font.SysFont('agencyfb', GAMEOVER_FONT_SIZE)
fontTitle = pygame.font.SysFont('agencyfb', TITLE_FONT_SIZE)
fontVersion = pygame.font.SysFont('agencyfb', VERSION_FONT_SIZE)
