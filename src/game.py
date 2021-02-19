import random
import time

import numpy as np

import config
from ball import Ball
from brick import Glass_brick, Super_Brick, Brick
from kbhit import KBHit
from paddle import Paddle
from powerup import PowerUp
from screen import Screen


class Game:

    def __init__(self):
        self.__screen = Screen()
        self.__paddle = Paddle()
        self.__balls = [Ball()]
        self.__lives = config.LIVES
        self.__bricks = []
        self.__super_bricks = []
        self.__unbreakable_cnt = 0
        self.__powers_falling = []
        self.__powers_expire = np.zeros(8)
        self.__loop = 1
        self.__game_speed = config.GAME_SPEED

        print("\033[?25l\033[2J")  # disappear cursor and clear screen

    def game_loop(self):
        kb_inp = KBHit()
        random.seed()
        _time_begin = time.time()
        _score = config.MAX_SCORE
        self.__populate_bricks()
        while self.__lives:
            self.__screen.clear()

            if config.DEBUG:
                print(self.__loop, "😁")
                print("\033[KBall: ", self.__balls[0].x, self.__balls[0].y, self.__balls[0].speed)
                print("\033[KPowers: ", self.__powers_expire)

            print("\033[KLives ❤", self.__lives)
            print("\033[KBricks left: ", len(self.__bricks + self.__super_bricks) - self.__unbreakable_cnt)
            print("\033[KTime Played: ", round(time.time() - _time_begin, 2), "seconds")
            _score = self.__calc_score(round(time.time() - _time_begin, 2),
                                              len(self.__bricks + self.__super_bricks) - self.__unbreakable_cnt)

            if _score <= 0:
                break
            print("\033[KScore: ", _score)

            self.__loop += 1

            if kb_inp.kbhit():
                inp_key = kb_inp.getch()
                if inp_key == config.QUIT_CHR:
                    break
                self.__handle_input(inp_key)
            # else:
            #     print('\033[K no key')

            kb_inp.clear()

            # Increase refresh rate for fast ball
            if config.DEBUG:
                self.__game_speed = 10000
            elif self.__is_pow_active(4):
                self.__game_speed = 1.5 * config.GAME_SPEED
            else:
                self.__game_speed = config.GAME_SPEED

            # Check power up effects on balls
            for ball in self.__balls:
                if self.__is_pow_active(5):
                    ball.set_looks(face="👺")
                else:
                    ball.reset_looks()

                if not self.__is_pow_active(6):
                    ball.paddle_rel_pos = int(self.__paddle.shape[0] / 2)
                else:
                    ball.paddle_rel_pos = min(ball.paddle_rel_pos, self.__paddle.shape[0] - 2)

            # Check power up effects on paddle
            if config.DEBUG:
                self.__paddle.set_looks(shape=[config.WIDTH, 2], face="🍄")
            elif self.__is_pow_active(1):
                self.__paddle.set_looks(shape=[28, 1], face="🌀")
            elif self.__is_pow_active(2):
                self.__paddle.set_looks(shape=[12, 1], face="📍")
            else:
                self.__paddle.reset_looks()

            self.__paddle.move(0)
            self.__draw(self.__paddle)

            for brick in self.__bricks + self.__super_bricks:
                self.__draw(brick)

            for power in self.__powers_falling:
                self.__draw(power)

            self.__fall_power_ups()
            self.__collateral()  # clean up bricks from list

            for ball in self.__balls:
                ball.move(2 * int((self.__paddle.x + ball.paddle_rel_pos) / 2), self.__paddle.y - 1)
                self.__check_collide(ball)

                if ball.y >= config.HEIGHT:
                    self.__balls.remove(ball)
                    # ball.freeze()
                    # ball.speed = [config.INIT_SPEED, -1]
                else:
                    self.__draw(ball)
                    # print('\033[K ', ball.x, ball.y, ball.speed, ball.moving, ball.paddle_rel_pos)
                    # if config.DEBUG:
                    #     with open("debug_print/ball_path.txt", "a") as f:
                    #         print(self.__loop, ball.x, ball.y, ball.speed, file=f)

            if len(self.__balls) == 0:
                self.__lives -= 1
                self.__powers_expire = np.zeros(8)  # reset powers on dying
                self.__balls = [Ball()]

            print('\033[31m', ''.join('X' for _ in range(config.WIDTH - 2)), '\033[0m')
            self.__screen.show()
            time.sleep(1 / self.__game_speed)
            if not config.DEBUG:
                if len(self.__bricks + self.__super_bricks) == 0:
                    break
        print('GAME OVER!')
        if len(self.__bricks + self.__super_bricks) <= self.__unbreakable_cnt:
            print("YOU WON! You Scored: ", _score)
        elif _score <= 0:
            print("YOU LOST! TIME is up.")

    def __collateral(self):
        for brick in self.__super_bricks:
            if brick.active:
                brick.explode(self.__super_bricks + self.__bricks)
                self.__super_bricks.remove(brick)
        for brick in self.__bricks:
            if brick.active:
                if not self.__is_pow_active(5):  # do not drop powerups if thru-ball is active
                    self.__powers_falling.append(PowerUp(x=brick.x, y=brick.y + 1, type=random.randint(1, 7)))
                if brick.__class__.__name__ == "Brick":
                    self.__unbreakable_cnt -= 1
                self.__bricks.remove(brick)

    def __check_collide(self, ball):
        # Walls
        ball.check_walls()

        # Paddle
        if ball.y >= self.__paddle.y - 1 and ball.x in range(self.__paddle.x - 1,
                                                             self.__paddle.x + self.__paddle.shape[0] - 1):
            if ball.moving:
                ball.reflect(1)  # Vertical
                ball.set_position(y=self.__paddle.y - 1)
                if not config.DEBUG:
                    ball.accelerate(2 * int((ball.x - (self.__paddle.x + int(self.__paddle.shape[0] / 2) - 1)) / 4))

                if self.__is_pow_active(6):
                    ball.freeze()
                    ball.paddle_rel_pos = ball.x - self.__paddle.x

        # Bricks
        for brick in self.__bricks:
            if (dir := ball.path_cut(brick)) != -1:
                if config.DEBUG:
                    with open("debug_print/brick_collide.txt", "a") as f:
                        print(self.__loop, brick.x, brick.y, file=f)

                if self.__is_pow_active(5):
                    brick.destroy()
                else:
                    ball.reflect(dir)
                    if hasattr(brick, 'level'):
                        brick.damage()
                        if brick.level <= 0:
                            brick.destroy()
                # break

        # Super Bricks
        for brick in self.__super_bricks:
            if (dir := ball.path_cut(brick)) != -1:
                brick.destroy()

    def __fall_power_ups(self):
        # PowerUps Falling
        for power in self.__powers_falling:
            power.y += 1
            if power.y >= config.HEIGHT - 2:
                if power.x in range(self.__paddle.x - 1, self.__paddle.x + self.__paddle.shape[0] - 1):
                    self.__powers_expire[power.type] = self.__loop + 300
                    if power.type == 1 or power.type == 2:
                        self.__powers_expire[3 - power.type] = 0  # long paddle means not short and vice versa
                    elif power.type == 4:
                        self.__powers_expire[power.type] = self.__loop + 300
                    elif power.type == 7:
                        self.__lives += 1
                    elif power.type == 3:
                        self.__duplicate_balls()
                self.__powers_falling.remove(power)

    def __populate_bricks(self):
        brick_list = []
        super_brick_list = []
        _x = 14
        _y = 10

        for block in range(0, 3):
            for grp in range(0, 18):
                # for grp in range(0, 8):
                if random.randint(1, 5) == 3:
                    for br in range(0, 5):
                        if grp % 3 != block % 3:
                            brick = {
                                "x": _x,
                                "y": _y,
                            }
                            super_brick_list.append(brick)
                            if grp % 3 == block % 3 + 1:
                                brick = {
                                    "x": _x - 4,
                                    "y": _y,
                                }
                                super_brick_list.append(brick)
                        _x += 2
                        # _x += 4
                        _y += 1 if grp % 2 else -1
                else:
                    for br in range(0, 5):
                        if grp % 3 != block % 3:
                            brick = {
                                "x": _x,
                                "y": _y,
                                "level": random.randint(1, 4)
                            }
                            brick_list.append(brick)
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
                    self.__bricks.append(Brick(obj['x'], obj['y']))
                    self.__unbreakable_cnt += 1
                elif random.randint(1, 10) == 3:
                    self.__super_bricks.append(Super_Brick(obj['x'], obj['y']))
                else:
                    self.__bricks.append(Glass_brick(obj['x'], obj['y'], obj['level']))

        for obj in super_brick_list:
            if obj['x'] + 4 <= config.WIDTH and obj['y'] <= config.HEIGHT - 5:
                self.__super_bricks.append(Super_Brick(obj['x'], obj['y']))

        # for brick in self.__super_bricks:
        #     with open("debug_print/bricks.txt", "a") as f:
        #         print(brick.x, brick.y, brick.__class__.__name__, file=f)

    # is this power active
    def __is_pow_active(self, type):
        return self.__powers_expire[type] > self.__loop

    def __duplicate_balls(self):
        if len(self.__balls) <= int(config.MAX_BALLS / 2):
            new_balls = []
            for ball in self.__balls:
                new_balls.append(Ball(x=ball.x, y=ball.y, speed=list(map(lambda x: -x, ball.speed)), moving=1))
            self.__balls.extend(new_balls)

    def __handle_input(self, ch):
        # print("\033[K Key pressed: ", ch)
        if ch == config.MOVE_LEFT:
            self.__paddle.move(-1)
        elif ch == config.MOVE_RIGHT:
            self.__paddle.move(1)
        elif ch == config.RELEASE:
            for ball in self.__balls:
                if not ball.moving:
                    ball.release()

    def __draw(self, obj):
        for row in range(obj.shape[1]):
            for col in range(obj.shape[0]):
                self.__screen.display[obj.y + row][obj.x + col] = obj.get_face if col % 2 else ""

    def __calc_score(self, time, bricks):
        return round(config.MAX_SCORE - time*10 - bricks*10)

    def __del__(self):
        self.__screen.clear()
        print("\033[?25h\033[2J")  # reappear cursor
