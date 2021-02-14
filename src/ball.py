from object import Object


class Ball(Object):
    def __init__(self):
        super().__init__([2, 1], "🎱")
        self.speed = 0
        self.direction = [0, 0]

    def release(self):
        self.speed = 1
        self.direction = [-1, -1]

    def set_position(self,x,y):
        self.x = x
        self.y = y

    def move(self, x=0, y=0):
        if self.speed == 0:
            self.set_position(x,y)
        else:
            self.set_position(self.x + self.direction[0] * self.speed, self.y + self.direction[1] * self.speed)

    ''' 
        0: Horizontal        
        1: Vertical
    '''

    def reflect(self, dir):
        self.direction[dir] *= -1

    def path_cut(self, obstacle) -> int:
        _now = self.x
        _next = self.x + self.direction[0] * self.speed + 1
        if self.direction[0] < 0:
            _now += 1
            _next -= 1
            _now = _next + _now
            _next = _now - _next
            _now = _now - _next
        if self.direction[0] != 0 and \
            (self.y <= obstacle.y <= self.y + self.direction[1] * self.speed or
             self.y >= obstacle.y >= self.y + self.direction[1] * self.speed):
            if self.x <= obstacle.x - 2 < self.x + self.direction[0] * self.speed:
                # self.y = obstacle.y
                # self.x = obstacle.x - 2
                self.set_position(obstacle.x - 2,obstacle.y)
                return 0
            if self.x >= obstacle.x + obstacle.shape[0] > self.x + self.direction[0] * self.speed:
                # self.y = obstacle.y
                # self.x = obstacle.x + obstacle.shape[0]
                self.set_position(obstacle.x + obstacle.shape[0],obstacle.y)
                return 0

        if self.direction[1] != 0 and max(_now, obstacle.x) <= min(_next, obstacle.x + obstacle.shape[0] - 1):
            if self.y <= obstacle.y < self.y + self.direction[1] * self.speed:
                self.set_position(self.x,obstacle.y - 1)
                return 1
            if self.y >= obstacle.y > self.y + self.direction[1] * self.speed:
                # self.y = obstacle.y + 1
                self.set_position(self.x,obstacle.y + 1)
                return 1
        return -1
