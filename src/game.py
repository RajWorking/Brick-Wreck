import time

import numpy as np

import config
from kbhit import KBHit
from paddle import Paddle
from screen import Screen
from ball import Ball


class Game:

    def __init__(self):
        self.screen = Screen()
        self.paddle = Paddle()
        self.ball = Ball()
        self.lives = 3
        print("\033[?25l\033[2J")  # disappear cursor and clear screen

    def game_loop(self):
        kb_inp = KBHit()
        c = 1
        while self.lives:
            self.screen.clear()
            print(c, "😁 lives: ", self.lives)
            c += 1

            if kb_inp.kbhit():
                inp_key = kb_inp.getch()
                if inp_key == config.QUIT_CHR:
                    break
                self.handle_input(inp_key)
                kb_inp.clear()
            else:
                print('\033[K no key')

            self.draw(self.paddle)

            self.ball.set_position(self.paddle.x + int(self.paddle.shape[0]/2),self.paddle.y-1)
            self.check_collide()

            if self.ball.y == config.HEIGHT:
                print('Dead')
                self.lives-=1
                self.ball.speed = 0
            else:
                self.draw(self.ball)

            print('\033[31m',''.join('X' for i in range(config.WIDTH - 2)),'\033[0m')
            self.screen.show()
            time.sleep(1/config.GAME_SPEED)

    def check_collide(self):
        # Walls
        if self.ball.y <= 0:
            self.ball.reflect(2) # Vertical
            self.ball.y = 0
        if self.ball.x <= 0 or self.ball.x >= config.WIDTH - 2:
            self.ball.reflect(1) # Horizontal
            self.ball.x = max(0, self.ball.x)
            self.ball.x = min(self.ball.x, config.WIDTH - 2)

        # Paddle
        if self.ball.y >= self.paddle.y - 1 and self.ball.x in range(self.paddle.x,self.paddle.x+self.paddle.shape[0]):
            self.ball.reflect(2) # Vertical
            self.ball.y = self.paddle.y - 1
            self.ball.direction[0] += int((self.ball.x - (self.paddle.x + int(self.paddle.shape[0]/2)))/2)

    def handle_input(self, ch):
        print("\033[K Key pressed: ", ch)
        if ch == config.MOVE_LEFT:
            self.paddle.move(-1)
        elif ch == config.MOVE_RIGHT:
            self.paddle.move(1)
        elif ch == config.RELEASE:
            if self.ball.speed == 0:
                self.ball.release()

    def draw(self, obj):
        print(obj.x, obj.y, getattr(obj,'direction',""))
        for row in range(obj.shape[1]):
            for col in range(obj.shape[0]):
                self.screen.display[int(obj.y) + row][int(obj.x) + col] = obj.face if col % 2 else ""

    def __del__(self):
        self.screen.clear()
        print("\033[?25h\033[2J")  # reappear cursor
        print('GAME OVER!')
