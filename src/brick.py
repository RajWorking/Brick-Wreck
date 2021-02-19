from object import Object


class Brick(Object):
    def __init__(self, x, y):
        super().__init__(shape=[4, 1], x=x, y=y, face="⬛")
        self._active = False  # active true means it is about to die

    def destroy(self):
        self._active = True

    @property
    def active(self):
        return self._active


class Glass_brick(Brick):
    def __init__(self, x, y, level):
        super().__init__(x, y)
        self.__level = level

    @property
    def level(self):
        return self.__level

    def damage(self):
        self.__level -= 1

    @property
    def get_face(self):
        if self.__level == 1:
            return "🟩"
        elif self.__level == 2:
            return "🟨"
        elif self.__level == 3:
            return "🟧"
        elif self.__level == 4:
            return "🟥"
        return " "


class Super_Brick(Brick):
    def __init__(self, x, y):
        super().__init__(x, y)

    @property
    def get_face(self):
        return "💥"

    def explode(self, bricks):
        x1 = self.x - self.shape[0]
        x2 = self.x + self.shape[0]
        y1 = self.y - self.shape[1]
        y2 = self.y + self.shape[1]
        for brick in bricks:
            if x1 <= brick.x <= x2 and y1 <= brick.y <= y2:
                brick.destroy()
                # with open("debug_print/brick_collide.txt", "a") as f:
                #     print(self.x, self.y, ' -- ', brick.x, brick.y, file=f)
