import pygame as pg
from pygame.locals import *

from .entity import Entity

MOVE_SPEED = 5.0
VELOCITY_ATTENUATION = 0.5

class Player(Entity):
    def __init__(self, x, y, images, pos_bounds, is_turn):
        self.img_idx = 0
        self.images = images
        self.image = self.images[self.img_idx]
        Entity.__init__(self, self.image, x, y)

        # Constraints
        self.pos_bounds = pos_bounds
        self.is_turn = is_turn

        # Status Fields
        self.health = 100
        self.power = 0
        self.xp = 0

        # Kinematic Quantities
        self.xv = 0.0
        self.yv = 0.0

    def update(self, pressed_keys):
        # TODO: Remove after debugging.
        if pressed_keys[K_s]:
            self.is_turn = not self.is_turn

        # Only act if it's your turn.
        if not self.is_turn:
            return

        # TODO: Invert screen space in the engine so positive y is in the right
        # direction.

        # Alter velocity from user input.
        if pressed_keys[K_UP]:
            self.yv -= MOVE_SPEED
        if pressed_keys[K_DOWN]:
            self.yv += MOVE_SPEED
        if pressed_keys[K_LEFT]:
            self.xv -= MOVE_SPEED
        if pressed_keys[K_RIGHT]:
            self.xv += MOVE_SPEED

        # Update position.
        self.x += self.xv
        self.y += self.yv
        self.clamp_pos_to_bounds()
        self.rect.bottomleft = (self.x, self.y)
        # Attenuate velocities.
        self.xv *= VELOCITY_ATTENUATION
        self.yv *= VELOCITY_ATTENUATION

    def clamp_pos_to_bounds(self):
        # NOTE: We can't use the Rect clamp function, because Rect's store
        # integral fields, and we need more precision.
        self_x = self.x
        self_y = self.y
        self_w = self.rect.w
        self_h = self.rect.h
        bound_x = self.pos_bounds.x
        bound_y = self.pos_bounds.y
        bound_w = self.pos_bounds.w
        bound_h = self.pos_bounds.h
        if self_x < bound_x:
            self.x = bound_x
            self.xv *= -10
        elif self_x + self_w > bound_x + bound_w:
            self.x = bound_x + bound_w - self_w
            self.xv *= -10
        if self_y - self_h < bound_y:
            self.y = bound_y + self_h
            self.yv *= -10
        elif self_y > bound_y + bound_h:
            self.y = bound_y + bound_h
            self.yv *= -10
