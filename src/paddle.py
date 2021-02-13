import config
from object import Object

class Paddle(Object):
    def __init__(self):
        if config.DEBUG:
            super().__init__([config.WIDTH,2], "💀")
            self.x = 0
        else:
            super().__init__([18, 2], "💀")
            self.x = int(config.WIDTH / 2)
        self.y = config.HEIGHT - 2
        self.speed = 2

    def move(self, dir):
        if dir == -1:
            self.x = max(self.x - self.speed, 0)
        elif dir == 1:
            self.x = min(self.x + self.speed, config.WIDTH - self.shape[0])