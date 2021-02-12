import sys

import numpy as np

import config


class Screen:
    '''Manage how screen gets refreshed by updating frames
    '''
    def clear(self):
        """Clear the current frame
        """
        self.display = np.full((config.HEIGHT, config.WIDTH), " ")
        print("\033[0;0H")  # bring cursor to upper left corner

    def show(self):
        """Display the current frame on the screen
        """
        out = "\033[48;5;195m"
        for row in range(config.HEIGHT):
            for col in range(config.WIDTH):
                out += self.display[row][col]
                # out += "😁"
                # out += str(self.k)  # + "\033[48;5;195m"
            # self.k = (self.k + 1) % 10
            out += "\n"
        out += "\033[0m"
        sys.stdout.write(out)
