import os

terminal_size = os.get_terminal_size()

DEBUG = False

WIDTH = 2 * int(terminal_size.columns / 2)
HEIGHT = terminal_size.lines - 8

GAME_SPEED = 15
LIVES = 2
INIT_SPEED = -2
MAX_BALLS = 6
LEV_BONUS = 200
LEVELS = 3

QUIT_CHR = 'q'
MOVE_LEFT = 'a'
MOVE_RIGHT = 'd'
RELEASE = 's'
SKIP_LEVEL = 'x'
