import pygame as pg
from pygame.locals import *

MOVE_SPEED = 5.0
VELOCITY_ATTENUATION = 0.5
PLAYER_SIZE = 50 # pixels

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, img_locs, bounded_region=None, is_turn=False):
        pg.sprite.Sprite.__init__(self, self.groups)
        self.img_idx = 0
        self.images = [pg.transform.scale(pg.image.load(img_loc), (PLAYER_SIZE,) * 2) for img_loc in img_locs]
        self.image = self.images[self.img_idx]
        self.rect = self.image.get_rect(center=(x, y))

        # Constraints
        self.bounded_region = bounded_region
        self.is_turn = is_turn

        # Status Fields
        self.health = 100
        self.power = 0
        self.xp = 0

        # Kinematic Quantities
        self.x = x
        self.y = y
        self.xv = 0.0
        self.yv = 0.0

    def update(self, pressed_keys):
        # TODO: Remove after debugging.
        if pressed_keys[K_s]:
            self.is_turn = not self.is_turn

        # Only act if its your turn.
        if not self.is_turn:
            return

        # TODO: Invert screen space in the engine so positive y is in the right direction.

        # Alter velocity from user input.
        if pressed_keys[K_UP]:
            self.yv -= MOVE_SPEED
        if pressed_keys[K_DOWN]:
            self.yv += MOVE_SPEED
        if pressed_keys[K_LEFT]:
            self.xv -= MOVE_SPEED
        if pressed_keys[K_RIGHT]:
            self.xv += MOVE_SPEED

        # TODO: Restrict movement to bounded region, and also so player (x, y) is treated as its center, not top-left of rect
        radius = PLAYER_SIZE / 2.0
        if self.bounded_region[0][0] + radius < self.x + self.xv < self.bounded_region[1][0] - radius:
            self.x += self.xv
        if self.bounded_region[0][1] + radius < self.y + self.yv < self.bounded_region[1][1] - radius:
            self.y += self.yv

        # Update position and attenuation.
        self.rect.center = (self.x, self.y)
        self.xv *= VELOCITY_ATTENUATION
        self.yv *= VELOCITY_ATTENUATION
