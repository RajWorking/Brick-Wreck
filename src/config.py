import os

terminal_size = os.get_terminal_size()

DEBUG = False

WIDTH = terminal_size.columns
HEIGHT = terminal_size.lines - 10

GAME_SPEED = 15
LIVES = 5
INIT_SPEED = -1

QUIT_CHR = 'q'
MOVE_LEFT = 'a'
MOVE_RIGHT = 'd'
RELEASE = 's'
