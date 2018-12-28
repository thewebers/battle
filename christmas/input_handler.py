import pygame as pg
from pygame.locals import *


class InputHandler:
    def __init__(self):
        self.pressed_keys = {}
        self.close_requested = False

    def update(self):
        # Poll the event queue.
        for event in pg.event.get():
            if event.type == KEYDOWN:
                self.pressed_keys[event.key] = True
            elif event.type == KEYUP:
                self.pressed_keys[event.key] = False
            # Check if they tryna leave.
            self.close_requested |= event.type == QUIT
            self.close_requested |= self.is_key_pressed(K_ESCAPE)
            if self.close_requested:
                return

    def is_key_pressed(self, key):
        return self.pressed_keys.get(key, False)

    def is_close_requested(self):
        return self.close_requested
