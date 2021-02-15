import random
import time

import config
from ball import Ball
from brick import Glass_brick
from kbhit import KBHit
from paddle import Paddle
from screen import Screen


class Game:

    def __init__(self):
        self.screen = Screen()
        self.paddle = Paddle()
        self.ball = Ball()
        self.lives = config.LIVES
        self.bricks = []
        self.loop = 1

        print("\033[?25l\033[2J")  # disappear cursor and clear screen

    def game_loop(self):
        kb_inp = KBHit()
        random.seed()
        self.populate_bricks()
        while self.lives:
            self.screen.clear()
            print(self.loop, "😁")

            print("\033[KLives ❤", self.lives)
            print("\033[KBricks left: ", len(self.bricks))
            self.loop += 1

            if kb_inp.kbhit():
                inp_key = kb_inp.getch()
                if inp_key == config.QUIT_CHR:
                    break
                self.handle_input(inp_key)
            else:
                print('\033[K no key')

            kb_inp.clear()

            self.draw(self.paddle)

            self.ball.move(self.paddle.x + int(self.paddle.shape[0] / 2), self.paddle.y - 1)
            self.check_collide()

            for brick in self.bricks:
                self.draw(brick)

            if self.ball.y >= config.HEIGHT:
                print('\033[K Dead')
                self.lives -= 1
                self.ball.moving = 0
            else:
                print('\033[K ', self.ball.x, self.ball.y, self.ball.speed, self.ball.moving)
                if config.DEBUG:
                    with open("debug_print/ball_path.txt", "a") as f:
                        print(self.loop, self.ball.x, self.ball.y, self.ball.speed, file=f)
                self.draw(self.ball)

            print('\033[31m', ''.join('X' for _ in range(config.WIDTH - 2)), '\033[0m')
            self.screen.show()
            time.sleep(1 / config.GAME_SPEED)

    def check_collide(self):
        # Walls
        if self.ball.y <= 0:
            self.ball.reflect(1)  # Vertical
            self.ball.y = 0
        if self.ball.x <= 0 or self.ball.x >= config.WIDTH - 2:
            self.ball.reflect(0)  # Horizontal
            self.ball.x = max(0, self.ball.x)
            self.ball.x = min(self.ball.x, config.WIDTH - 2)

        # Paddle
        if self.ball.y >= self.paddle.y - 1 and self.ball.x in range(self.paddle.x - 1,
                                                                     self.paddle.x + self.paddle.shape[0] - 1):
            self.ball.reflect(1)  # Vertical
            self.ball.y = self.paddle.y - 1
            if not config.DEBUG:
                self.ball.speed[0] += int((self.ball.x - (self.paddle.x + int(self.paddle.shape[0] / 2) - 1)) / 2)

        # Bricks
        for brick in self.bricks:
            if (dir := self.ball.path_cut(brick)) != -1:
                self.ball.reflect(dir)
                if config.DEBUG:
                    with open("debug_print/brick_collide.txt", "a") as f:
                        print(self.loop, brick.x, brick.y, brick.level, file=f)

                brick.level -= 1
                if brick.level <= 0:
                    self.bricks.remove(brick)
                # break

    def populate_bricks(self):
        brick_list = []
        _x = 15
        _y = 10

        for block in range(0, 3):
            for grp in range(0, 18):
                for br in range(0, 5):
                    if grp % 3 != block % 3:
                        brick = {
                            "x": _x,
                            "y": _y,
                            "level": random.randint(1, 4)
                        }
                        brick_list.append(brick)
                        if config.DEBUG:
                            with open("debug_print/bricks.txt", "a") as f:
                                print(brick, file=f)
                    _x += 2
                    # _x += 4
                    _y += 1 if grp % 2 else -1
            _y += 5
            # _y += 1
            _x = 15

        # brick_list = [
        #     {
        #         "x": 26,
        #         "y": 10,
        #         "level": 3
        #     },
        #     {
        #         "x": 52,
        #         "y": 10,
        #         "level": 3
        #     }
        # ]

        for obj in brick_list:
            if obj['x'] + 4 <= config.WIDTH and obj['y'] <= config.HEIGHT - 5:
                self.bricks.append(Glass_brick(obj['x'], obj['y'], obj['level']))

    def handle_input(self, ch):
        print("\033[K Key pressed: ", ch)
        if ch == config.MOVE_LEFT:
            self.paddle.move(-1)
        elif ch == config.MOVE_RIGHT:
            self.paddle.move(1)
        elif ch == config.RELEASE:
            if self.ball.moving == 0:
                self.ball.release()

    def draw(self, obj):
        for row in range(obj.shape[1]):
            for col in range(obj.shape[0]):
                self.screen.display[obj.y + row][obj.x + col] = obj.get_face() if col % 2 else ""

    def __del__(self):
        self.screen.clear()
        print("\033[?25h\033[2J")  # reappear cursor
        print('GAME OVER!')
