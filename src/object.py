class Object:
    def __init__(self, shape, face="🚫", speed=None, x=0, y=0):
        if speed is None:
            speed = [0, 0]
        self.shape = shape
        self._face = face
        self.speed = speed
        self.set_position(x, y)

    def get_face(self):
        return self._face

    def set_looks(self, shape=None, face=None):
        if shape is not None:
            self.shape = shape
        if face is not None:
            self._face = face

    def set_position(self, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
