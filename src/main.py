import os

import config
from game import Game

if __name__ == "__main__":
    if config.DEBUG:
        for file in os.listdir('debug_print'):
            os.remove("debug_print/" + file)
    Game().game_loop()
