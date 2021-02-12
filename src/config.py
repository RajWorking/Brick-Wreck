import os

terminal_size = os.get_terminal_size()

WIDTH = terminal_size.columns
HEIGHT = terminal_size.lines - 7

GAME_SPEED = 10

QUIT_CHR = 'q'
MOVE_LEFT = 'a'
MOVE_RIGHT = 'd'
RELEASE = 's'