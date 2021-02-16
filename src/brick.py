from object import Object


class Brick(Object):
    def __init__(self, x, y):
        super().__init__(shape=[4, 1], x=x, y=y, face="⬛")


class Glass_brick(Brick):
    def __init__(self, x, y, level):
        super().__init__(x, y)
        self.level = level
        self.face = self.get_face()

    def get_face(self):
        if self.level == 1:
            return "🟩"
        elif self.level == 2:
            return "🟨"
        elif self.level == 3:
            return "🟧"
        elif self.level == 4:
            return "🟥"
        return " "
