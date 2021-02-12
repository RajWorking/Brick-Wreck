class Ball:
    def __init__(self):
        self.shape = [2, 1]
        self.face = "🎱"
        self.speed = 0
        self.direction = [0, 0]

    def release(self):
        self.speed = 1
        self.direction = [-1, -1]

    def set_position(self, x, y):
        if self.speed == 0:
            self.x = x
            self.y = y
        else:
            self.x = self.x + self.direction[0] * self.speed
            self.y = self.y + self.direction[1] * self.speed
            # upd_x = max(self.x + self.direction[0]*self.speed, 0)
            # upd_x = min(upd_x, config.WIDTH - 2)
            # upd_y = max(self.y + self.direction[1] * self.speed, 0)
            # upd_y = min(upd_y, config.HEIGHT-3)
            #
            # self.x = upd_x
            # self.y = upd_y

    ''' 
        1: Horizontal        
        2: Vertical
    '''

    def reflect(self, dir):
        if dir == 1:
            self.direction[0] *= -1
        elif dir == 2:
            self.direction[1] *= -1
