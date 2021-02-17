import config
from object import Object


class Paddle(Object):
    def __init__(self):
        if config.DEBUG:
            super().__init__(shape=[config.WIDTH, 2], face="💀", speed=[4, 0], x=0, y=config.HEIGHT - 2)
        else:
            super().__init__(shape=[20, 2], face="💀", speed=[4, 0], x=int(config.WIDTH / 2), y=config.HEIGHT - 2)

    def move(self, dir):
        if dir == -1:
            self.set_position(x=max(self.x - self.speed[0], 0))
        elif dir == 1:
            self.set_position(x=min(self.x + self.speed[0], config.WIDTH - self.shape[0]))
        else:
            self.set_position(x=max(min(self.x, config.WIDTH - self.shape[0]), 0))

    def reset_looks(self):
        self.set_looks(shape=[20, 2], face="💀")
