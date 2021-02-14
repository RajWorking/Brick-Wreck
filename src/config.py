import os

terminal_size = os.get_terminal_size()

DEBUG = True

WIDTH = terminal_size.columns
HEIGHT = terminal_size.lines - 10

GAME_SPEED = 100
LIVES = 5

QUIT_CHR = 'q'
MOVE_LEFT = 'a'
MOVE_RIGHT = 'd'
RELEASE = 's'