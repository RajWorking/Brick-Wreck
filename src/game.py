import random
import time

import numpy as np

import config
from ball import Ball
from brick import Glass_brick, Brick
from kbhit import KBHit
from paddle import Paddle
from powerup import PowerUp
from screen import Screen


class Game:

    def __init__(self):
        self.screen = Screen()
        self.paddle = Paddle()
        self.balls = [Ball()]
        self.lives = config.LIVES
        self.bricks = []
        self.powers_falling = []
        self.powers_expire = np.zeros(8)
        self.loop = 1
        self.game_speed = config.GAME_SPEED

        print("\033[?25l\033[2J")  # disappear cursor and clear screen

    def game_loop(self):
        kb_inp = KBHit()
        random.seed()
        self.populate_bricks()
        while self.lives:
            self.screen.clear()
            print(self.loop, "😁")

            print("\033[KLives ❤", self.lives, self.game_speed)
            print("\033[KBricks left: ", len(self.bricks))
            print("\033[KBall: ", self.balls[0].x, self.balls[0].y, self.balls[0].speed)
            print("\033[KPowers: ", self.powers_expire)
            self.loop += 1

            if kb_inp.kbhit():
                inp_key = kb_inp.getch()
                if inp_key == config.QUIT_CHR:
                    break
                self.handle_input(inp_key)
            else:
                print('\033[K no key')

            kb_inp.clear()

            # Increase refresh rate for fast ball
            if config.DEBUG:
                self.game_speed = 10000
            elif self.is_pow_active(4):
                self.game_speed = 1.5 * config.GAME_SPEED
            else:
                self.game_speed = config.GAME_SPEED

            # Check power up effects on balls
            for ball in self.balls:
                if self.is_pow_active(5):
                    ball.set_looks(face="👺")
                else:
                    ball.reset_looks()

                if not self.is_pow_active(6):
                    ball.paddle_rel_pos = int(self.paddle.shape[0] / 2)
                else:
                    ball.paddle_rel_pos = min(ball.paddle_rel_pos, self.paddle.shape[0] - 2)

            # Check power up effects on paddle
            if config.DEBUG:
                self.paddle.set_looks(shape=[config.WIDTH, 2], face="🍄")
            elif self.is_pow_active(1):
                self.paddle.set_looks(shape=[28, 1], face="🌀")
            elif self.is_pow_active(2):
                self.paddle.set_looks(shape=[12, 1], face="📍")
            else:
                self.paddle.reset_looks()

            self.paddle.move(0)
            self.draw(self.paddle)

            for brick in self.bricks:
                self.draw(brick)

            for power in self.powers_falling:
                self.draw(power)

            self.fall_power_ups()

            for ball in self.balls:
                ball.move(self.paddle.x + ball.paddle_rel_pos, self.paddle.y - 1)
                self.check_collide(ball)

                if ball.y >= config.HEIGHT:
                    self.balls.remove(ball)
                    # ball.freeze()
                    # ball.speed = [config.INIT_SPEED, -1]
                else:
                    self.draw(ball)
                    # print('\033[K ', ball.x, ball.y, ball.speed, ball.moving, ball.paddle_rel_pos)
                    # if config.DEBUG:
                    #     with open("debug_print/ball_path.txt", "a") as f:
                    #         print(self.loop, ball.x, ball.y, ball.speed, file=f)

            if len(self.balls) == 0:
                self.lives -= 1
                self.powers_expire = np.zeros(8)  # reset powers on dying
                self.balls = [Ball()]

            print('\033[31m', ''.join('X' for _ in range(config.WIDTH - 2)), '\033[0m')
            self.screen.show()
            time.sleep(1 / self.game_speed)
            if not config.DEBUG:
                if len(self.bricks) == 0:
                    break
        print('GAME OVER!')
        if len(self.bricks) == 0:
            print("YOU WON!")

    def check_collide(self, ball):
        # Walls
        ball.check_walls()

        # Paddle
        if ball.y >= self.paddle.y - 1 and ball.x in range(self.paddle.x - 1,
                                                           self.paddle.x + self.paddle.shape[0] - 1):
            if ball.moving:
                ball.reflect(1)  # Vertical
                ball.set_position(y=self.paddle.y - 1)
                if not config.DEBUG:
                    ball.speed[0] += 2 * int(
                        (ball.x - (self.paddle.x + int(self.paddle.shape[0] / 2) - 1)) / 4)

                if self.is_pow_active(6):
                    ball.freeze()
                    ball.paddle_rel_pos = ball.x - self.paddle.x

        # Bricks
        for brick in self.bricks:
            if (dir := ball.path_cut(brick)) != -1:

                if self.is_pow_active(5):
                    brick.level = 0
                else:
                    ball.reflect(dir)
                    if config.DEBUG:
                        with open("debug_print/brick_collide.txt", "a") as f:
                            print(self.loop, brick.x, brick.y, file=f)
                    if hasattr(brick, 'level'):
                        brick.level -= 1

                if hasattr(brick, 'level') and brick.level <= 0:
                    if not self.is_pow_active(5):  # do not drop powerups if thru-ball is active
                        self.powers_falling.append(PowerUp(x=brick.x, y=brick.y + 1, type=random.randint(1, 7)))

                    self.bricks.remove(brick)
                # break

    def fall_power_ups(self):
        # PowerUps Falling
        for power in self.powers_falling:
            power.y += 1
            if power.y >= config.HEIGHT - 2:
                if power.x in range(self.paddle.x - 1, self.paddle.x + self.paddle.shape[0] - 1):
                    self.powers_expire[power.type] = self.loop + 300
                    if power.type == 1 or power.type == 2:
                        self.powers_expire[3 - power.type] = 0  # long paddle means not short and vice versa
                    elif power.type == 4:
                        self.powers_expire[power.type] = self.loop + 300
                    elif power.type == 7:
                        self.lives += 1
                    elif power.type == 3:
                        self.duplicate_balls()
                self.powers_falling.remove(power)

    def populate_bricks(self):
        brick_list = []
        _x = 14
        _y = 10

        for block in range(0, 3):
            for grp in range(0, 18):
                # for grp in range(0, 8):
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
            _x = 14

        # brick_list = [
        #     {
        #         "x": 92,
        #         "y": 36,
        #         "level": 1
        #     },
        #     {
        #         "x": 96,
        #         "y": 36,
        #         "level": 2
        #     },
        #     {
        #         "x": 100,
        #         "y": 36,
        #         "level": 3
        #     },
        #     {
        #         "x": 104,
        #         "y": 36,
        #         "level": 4
        #     }
        # ]

        for obj in brick_list:
            if obj['x'] + 4 <= config.WIDTH and obj['y'] <= config.HEIGHT - 5:
                if random.randint(1, 10) == 7:
                    self.bricks.append(Brick(obj['x'], obj['y']))
                else:
                    self.bricks.append(Glass_brick(obj['x'], obj['y'], obj['level']))

    # is this power active
    def is_pow_active(self, type):
        return self.powers_expire[type] > self.loop

    def duplicate_balls(self):
        if len(self.balls) <= int(config.MAX_BALLS / 2):
            new_balls = []
            for ball in self.balls:
                new_balls.append(Ball(x=ball.x, y=ball.y, speed=list(map(lambda x: -x, ball.speed)), moving=1))
            self.balls.extend(new_balls)

    def handle_input(self, ch):
        print("\033[K Key pressed: ", ch)
        if ch == config.MOVE_LEFT:
            self.paddle.move(-1)
        elif ch == config.MOVE_RIGHT:
            self.paddle.move(1)
        elif ch == config.RELEASE:
            for ball in self.balls:
                if not ball.moving:
                    ball.release()

    def draw(self, obj):
        for row in range(obj.shape[1]):
            for col in range(obj.shape[0]):
                self.screen.display[obj.y + row][obj.x + col] = obj.get_face() if col % 2 else ""

    def __del__(self):
        self.screen.clear()
        print("\033[?25h\033[2J")  # reappear cursor
