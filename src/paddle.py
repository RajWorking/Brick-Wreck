import config

class Paddle:
    def __init__(self):
        self.x = int(config.WIDTH / 2)
        self.y = config.HEIGHT - 2
        self.shape = [14,1]
        self.speed = 2
        self.face = "💀"
    
    def move(self, dir):
        if dir == -1:
            self.x = max(self.x - self.speed, 0)
        elif dir == 1:
            self.x = min(self.x + self.speed, config.WIDTH - self.shape[0])