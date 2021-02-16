from object import Object

'''
0. None
1. Expand Paddle
2. Shrink Paddle
3. Ball Multiplier
4. Fast Ball
5. Thru-Ball
6. Paddle Grab
7. Increase Life
'''


class PowerUp(Object):
    def __init__(self, x, y, type):
        super().__init__(shape=[2, 1], speed=[0, 1], x=x, y=y)
        self.type = type
        self.face = self.get_face()

    powers = {
        1: "🥕", # carrot
        2: "🍋", # lemon
        3: "🍇", # grapes
        4: "⏰", # alarm clock
        5: "💣", # bomb
        6: "🍓", # strawberry
        7: "💝", # heart
    }

    def get_face(self):
        if self.type not in range(1, 7):
            return "🦞"
        return self.__class__.powers[self.type]
