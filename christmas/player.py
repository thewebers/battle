import pygame as pg
from pygame.locals import *

MOVE_SPEED = 5.0
VELOCITY_ATTENUATION = 0.5


class Player(pg.sprite.Sprite):
    images = []

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self, self.groups)
        self.img_idx = 0
        self.image = self.images[self.img_idx]
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.x = x
        self.y = y
        # Velocity
        self.xv = 0.0
        self.yv = 0.0

    def update(self, pressed_keys):
        # TODO: Invert screen space in the engine so positive y is in the right
        # direction.
        if pressed_keys[K_UP]:
            self.yv -= MOVE_SPEED
        elif pressed_keys[K_DOWN]:
            self.yv += MOVE_SPEED
        elif pressed_keys[K_LEFT]:
            self.xv -= MOVE_SPEED
        elif pressed_keys[K_RIGHT]:
            self.xv += MOVE_SPEED
        self.x += self.xv
        self.y += self.yv
        self.rect[0] = self.x
        self.rect[1] = self.y
        self.xv *= VELOCITY_ATTENUATION
        self.yv *= VELOCITY_ATTENUATION

        self.img_idx = (self.img_idx + 1) % len(self.images)
        self.image = self.images[self.img_idx]

    def get_surface(self):
        return self.images[self.img_idx]
