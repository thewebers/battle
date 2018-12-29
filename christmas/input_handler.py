from enum import Enum

import pygame as pg
from pygame.locals import *


class InputIntent(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    FIRE = 4
    CHOOSE_MOVE_ONE = 5
    CHOOSE_MOVE_TWO = 6
    CHOOSE_MOVE_THREE = 7


TOP_PLAYER_INPUT_CONFIG = {
    InputIntent.UP: K_w,
    InputIntent.DOWN: K_s,
    InputIntent.LEFT: K_a,
    InputIntent.RIGHT: K_d,
    InputIntent.FIRE: K_e,
    InputIntent.CHOOSE_MOVE_ONE: K_1,
    InputIntent.CHOOSE_MOVE_TWO: K_2,
    InputIntent.CHOOSE_MOVE_THREE: K_3,
}


BOTTOM_PLAYER_INPUT_CONFIG = {
    InputIntent.UP: K_UP,
    InputIntent.DOWN: K_DOWN,
    InputIntent.LEFT: K_LEFT,
    InputIntent.RIGHT: K_RIGHT,
    InputIntent.FIRE: K_COMMA,
    InputIntent.CHOOSE_MOVE_ONE: K_k,
    InputIntent.CHOOSE_MOVE_TWO: K_l,
    InputIntent.CHOOSE_MOVE_THREE: K_SEMICOLON,
}


class InputHandler:
    def __init__(self):
        self.pressed_keys = {}
        self.last_pressed_keys = {}
        self.close_requested = False

    def update(self):
        self.last_pressed_keys = self.pressed_keys.copy()
        # Poll the event queue.
        for event in pg.event.get():
            if event.type == KEYDOWN:
                self.pressed_keys[event.key] = True
            elif event.type == KEYUP:
                self.pressed_keys[event.key] = False
            # Check if they tryna leave.
            self.close_requested |= event.type == QUIT
            self.close_requested |= self.is_key_down(K_ESCAPE)
            if self.close_requested:
                return

    def is_key_pressed(self, key):
        return (self.pressed_keys.get(key, False) and
                not self.last_pressed_keys.get(key, False))

    def is_key_down(self, key):
        return self.pressed_keys.get(key, False)

    def is_close_requested(self):
        return self.close_requested
