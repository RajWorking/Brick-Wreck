import config
from object import Object


class Paddle(Object):
    def __init__(self):
        if config.DEBUG:
            super().__init__(shape=[config.WIDTH, 2], face="💀", speed=[2, 0], x=0, y=config.HEIGHT - 2)
        else:
            super().__init__(shape=[20, 2], face="💀", speed=[2, 0], x=int(config.WIDTH / 2), y=config.HEIGHT - 2)

    def move(self, dir):
        if dir == -1:
            self.x = max(self.x - self.speed[0], 0)
        elif dir == 1:
            self.x = min(self.x + self.speed[0], config.WIDTH - self.shape[0])
