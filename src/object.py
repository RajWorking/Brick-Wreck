class Object:
    def __init__(self, shape, face="🚫"):
        self.shape = shape
        self.face = face

    def get_face(self):
        return self.face