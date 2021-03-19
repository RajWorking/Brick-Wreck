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
        self.__loop = 1
        self.__paddle = Paddle()
        self.__balls = [Ball()]
        self.__bricks = []
        self.__super_bricks = []
        self.__unbreakable_cnt = 0
        self.__powers_falling = []
        self.__powers_expire = np.zeros(8)
        self.__game_speed = config.GAME_SPEED
        self.__lives = config.LIVES
        self.__level = 0
        self.__score = config.LEV_BONUS
        self.__tot_score = 0
        self.__dead_msg = ""

        print("\033[?25l\033[2J")  # disappear cursor and clear screen

    def game_loop(self):
        self.kb_inp = KBHit()
        random.seed()

        while self.is_alive:
            self.reset_level()
            while len(self.get_all_bricks()) - self.__unbreakable_cnt:
                self.__screen.clear()
                self.__loop += 1

                if self.kb_inp.kbhit():
                    inp_key = self.kb_inp.getch()
                    self.__handle_input(inp_key)
                    if inp_key == config.QUIT_CHR:
                        self.__level = 100
                        break
                    elif inp_key == config.SKIP_LEVEL:
                        break
                # else:
                #     print('\033[K no key')
                self.kb_inp.clear()

                if config.DEBUG:
                    print(self.__loop, "😁")
                    print("\033[KBall: ", self.__balls[0].x, self.__balls[0].y, self.__balls[0].speed)
                    print("\033[KPowers: ", self.__powers_expire)

                print("\033[KLives ❤", self.__lives)
                print("\033[KLevel 🔱", self.__level)
                print("\033[KBricks left: ", len(self.get_all_bricks()) - self.__unbreakable_cnt)
                print("\033[KTime Played: ", round(time.time() - self.__time_begin, 2), "seconds")
                self.__score = self.__tot_score + self.__calc_score(round(time.time() - self.__time_begin, 2),
                                                                    len(self.get_all_bricks()))
                print("\033[KScore: ", self.__score)

                self.play_level()

                if not self.is_alive:
                    break

            if not self.is_alive:
                break
            self.__level += 1
            self.__tot_score = self.__score

        print('GAME OVER! Thanks for playing.')
        if self.__level <= config.LEVELS:
            print('You reached level', self.__level)
        elif self.__level == config.LEVELS + 1:
            print('All levels completed.')
        print(self.__dead_msg)

    @property
    def is_alive(self):
        if self.__level > config.LEVELS:
            self.__dead_msg = "YOU WON! You Scored: " + str(self.__tot_score)
            return False
        if self.__score <= 0:
            self.__dead_msg = "YOU LOST! TIME is up."
            return False
        if self.__lives <= 0:
            self.__dead_msg = "YOU LOST! All lives are over."
            return False

        for brick in self.get_all_bricks():
            if brick.y >= config.HEIGHT - 3:
                self.__dead_msg = "YOU LOST! Bricks too close."
                return False  # instant death

        return True

    def play_level(self):

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

        for brick in self.get_all_bricks():
            self.__draw(brick)

        for brick in self.__bricks:
            if hasattr(brick, 'level'):
                brick.change_level()

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

    def get_all_bricks(self):
        return self.__bricks + self.__super_bricks

    def reset_level(self):
        self.__time_begin = time.time()
        self.__loop = 1
        self.__unbreakable_cnt = 0
        self.__populate_bricks()
        self.__tot_bricks = len(self.get_all_bricks())
        self.__powers_expire = np.zeros(8)
        self.__powers_falling = []
        self.__balls = [Ball()]

    def falling_bricks(self):
        for brick in self.get_all_bricks():
            brick.fall()

    def __collateral(self):
        for brick in self.__super_bricks:
            if brick.active:
                brick.explode(self.__super_bricks + self.__bricks)
                self.__super_bricks.remove(brick)
                # with open("debug_print/super_brick.txt", "a") as f:
                #     print(self.__loop, brick.x, brick.y, brick.__class__.__name__, file=f)
                break

        for brick in self.__bricks:
            if brick.active:
                if not self.__is_pow_active(5):  # do not drop powerups if thru-ball is active
                    self.__powers_falling.append(
                        PowerUp(x=brick.x, y=brick.y + 1, type=random.randint(1, 7), speed=brick.proj_vel))
                if brick.__class__.__name__ == "Brick":
                    self.__unbreakable_cnt -= 1
                self.__bricks.remove(brick)
                break

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

                if self.__loop > config.TRIGGER_FALL:
                    self.falling_bricks()

        # Bricks
        for brick in self.__bricks:
            if (dir := ball.path_cut(brick)) != -1:
                if config.DEBUG:
                    with open("debug_print/brick_collide.txt", "a") as f:
                        print(self.__loop, brick.x, brick.y, file=f)

                if self.__is_pow_active(5):
                    brick.destroy(ball.speed.copy())
                else:
                    ball.reflect(dir)
                    if hasattr(brick, 'level'):
                        brick.damage()
                        if brick.level <= 0:
                            brick.destroy(ball.speed.copy())
                break

        # Super Bricks
        for brick in self.__super_bricks:
            if (dir := ball.path_cut(brick)) != -1:
                brick.destroy(ball.speed.copy())
                break

    def __fall_power_ups(self):
        # PowerUps Falling
        for power in self.__powers_falling:
            power.set_position(power.x + power.speed[0], power.y + round(power.speed[1]))
            power.inc_speed(v=min(1, power.speed[1] + 1))

            power.check_walls()

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
        self.__bricks = []
        self.__super_bricks = []

        if self.__level == 1:
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
        elif self.__level == 2:
            _x = 20
            _y = 10

            for block in range(0, 10):
                if random.randint(1, 5) == 3:
                    _y = 8
                    for grp in range(0, 20):
                        brick = {
                            "x": _x,
                            "y": _y,
                        }
                        super_brick_list.append(brick)
                        _y += 1
                else:
                    _y = 4
                    for grp in range(0, 25):
                        brick = {
                            "x": _x,
                            "y": _y,
                            "level": random.randint(1, 4)
                        }
                        brick_list.append(brick)
                        _y += 1
                _x += 16
        elif self.__level == 3:
            _y = 5

            for block in range(0, 7):
                if random.randint(1, 3) == 3:
                    _x = 20
                    for grp in range(0, 40):
                        brick = {
                            "x": _x,
                            "y": _y,
                        }
                        super_brick_list.append(brick)
                        _x += 4
                else:
                    _x = 10
                    for grp in range(0, 45):
                        brick = {
                            "x": _x,
                            "y": _y,
                            "level": random.randint(1, 4)
                        }
                        brick_list.append(brick)
                        _x += 4
                _y += 4
        else:
            brick_list = [
                {
                    "x": 92,
                    "y": 36,
                    "level": 2
                },
                {
                    "x": 96,
                    "y": 36,
                    "level": 2
                },
                {
                    "x": 100,
                    "y": 36,
                    "level": 3
                },
                {
                    "x": 104,
                    "y": 36,
                    "level": 4
                }
            ]

        for obj in brick_list:
            if obj['x'] + 4 <= config.WIDTH and obj['y'] <= config.HEIGHT - 5:
                if random.randint(1, 10) == 7:
                    self.__bricks.append(Brick(obj['x'], obj['y']))
                    self.__unbreakable_cnt += 1
                elif random.randint(1, 10) == 3:
                    self.__super_bricks.append(Super_Brick(obj['x'], obj['y']))
                else:
                    self.__bricks.append(Glass_brick(obj['x'], obj['y'], obj['level']))
                    if random.randint(1, 10) < 3:
                        self.__bricks[-1].set_rainbow()

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
                # with open('debug_print/blah.txt', 'a') as f:
                #     print(obj.__class__.__name__, obj.x, obj.y, obj.speed, file=f)
                self.__screen.display[obj.y + row][obj.x + col] = obj.get_face if col % 2 else ""

    def __calc_score(self, time, bricks):
        return round(config.LEV_BONUS - time * 10 + (self.__tot_bricks - bricks) * 10)

    def __del__(self):
        self.__screen.clear()
        print("\033[?25h\033[2J")  # reappear cursor
