import config
from object import Object


class Ball(Object):
    def __init__(self, x=0, y=0, speed=None, moving=0):
        if speed is None:
            speed = [config.INIT_SPEED, -1]
        super().__init__(shape=[2, 1], face="🎱", speed=speed, x=x, y=y)
        self.moving = moving
        self.paddle_rel_pos = 0  # relative position of ball on paddle

    def release(self):
        self.moving = 1

    def freeze(self):
        self.moving = 0

    def reset_looks(self):
        self.set_looks(face="🎱")

    def move(self, x=0, y=0):
        if self.moving == 0:
            self.set_position(x, y)
        else:
            self.set_position(self.x + self.speed[0], self.y + self.speed[1])

    def check_walls(self):
        if self.y <= 0:
            self.reflect(1)  # Vertical
            self.set_position(y=0)
        if self.x <= 0 or self.x >= config.WIDTH - 2:
            self.reflect(0)  # Horizontal
            self.set_position(x=min(max(0, self.x), config.WIDTH - 2))

    ''' 
        0: Horizontal        
        1: Vertical
    '''

    def reflect(self, dir):
        self.speed[dir] *= -1

    def accelerate(self, speedup):
        self.speed[0] += speedup

    @staticmethod
    def check_intersect(x1, x2):
        x1.sort()
        x2.sort()
        if max(x1[0], x2[0]) <= min(x1[1], x2[1]):
            return True
        return False

    def path_cut(self, obstacle) -> int:
        x1 = self.x
        x2 = self.x + self.speed[0] + 1
        if self.speed[0] < 0:
            x1 = self.x + self.speed[0]
            x2 = self.x + 1
        if self.speed[0] != 0 and \
                (self.y <= obstacle.y <= self.y + self.speed[1] or
                 self.y >= obstacle.y >= self.y + self.speed[1]):
            if self.x <= obstacle.x - 2 < self.x + self.speed[0]:
                self.set_position(obstacle.x - 2, obstacle.y)
                return 0
            if self.x >= obstacle.x + obstacle.shape[0] > self.x + self.speed[0]:
                self.set_position(obstacle.x + obstacle.shape[0], obstacle.y)
                return 0

        if self.speed[1] != 0 and self.check_intersect([x1, x2], [obstacle.x, obstacle.x + obstacle.shape[0] - 1]):
            if self.y <= obstacle.y < self.y + self.speed[1]:
                self.set_position(y=obstacle.y - 1)
                return 1
            if self.y >= obstacle.y > self.y + self.speed[1]:
                self.set_position(y=obstacle.y + 1)
                return 1
        return -1
