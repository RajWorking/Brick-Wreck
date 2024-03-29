from object import Object


class Brick(Object):
    def __init__(self, x, y):
        super().__init__(shape=[4, 1], x=x, y=y, face="⬛")
        self._active = False  # active true means it is about to die
        self.__proj_vel = [2, 1]  # projectile velocity

    @property
    def proj_vel(self):
        return self.__proj_vel

    def destroy(self, vel=None):
        if vel is None:
            vel = [0, 1]
        self._active = True
        self.__proj_vel = vel

    def fall(self):
        self.set_position(y=self.y + 1)

    @property
    def active(self):
        return self._active


class Glass_brick(Brick):
    def __init__(self, x, y, level):
        super().__init__(x, y)
        self.__level = level
        self.__rainbow = False

    def set_rainbow(self):
        self.__rainbow = True

    @property
    def level(self):
        return self.__level

    def change_level(self):
        if self.__rainbow:
            self.__level = 1 + (self.__level) % 4

    def damage(self):
        if not self.__rainbow:
            self.__level -= 1
        self.__rainbow = False

    @property
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
                with open("debug_print/brick_collide.txt", "a") as f:
                    print(self.x, self.y, ' -- ', brick.x, brick.y, file=f)
