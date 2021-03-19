import config


class Object:
    def __init__(self, shape, face="🚫", speed=None, x=0, y=0):
        if speed is None:
            speed = [0, 0]
        self._shape = shape
        self._face = face
        self._speed = speed
        self.set_position(x, y)

    @property
    def get_face(self):
        return self._face

    @property
    def speed(self):
        return self._speed

    def inc_speed(self, u=None, v=None):
        if u is not None:
            self._speed[0] = u
        if v is not None:
            self._speed[1] = v

    @property
    def shape(self):
        return self._shape

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
        self._speed[dir] *= -1

    def set_looks(self, shape=None, face=None):
        if shape is not None:
            self._shape = shape
        if face is not None:
            self._face = face

    def set_position(self, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
