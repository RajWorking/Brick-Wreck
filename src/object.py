class Object:
    def __init__(self, shape, face="🚫", speed=None, x=0, y=0):
        if speed is None:
            speed = [0, 0]
        self.shape = shape
        self.face = face
        self.speed = speed
        self.x = x
        self.y = y

    def get_face(self):
        return self.face
