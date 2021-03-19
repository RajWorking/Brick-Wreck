import os

terminal_size = os.get_terminal_size()

DEBUG = False

WIDTH = 2 * int(terminal_size.columns / 2)
HEIGHT = terminal_size.lines - 8

GAME_SPEED = 15
LIVES = 2
INIT_SPEED = 0
MAX_BALLS = 6
LEV_BONUS = 500
LEVELS = 3
TRIGGER_FALL = 200

QUIT_CHR = 'q'
MOVE_LEFT = 'a'
MOVE_RIGHT = 'd'
RELEASE = 's'
SKIP_LEVEL = 'x'
