import pygame as pg

from .entity import Entity
from .player import Player

# TODO: Make Santa a bot.

class Santa(Player):
    # Number of ticks to wait between animation frames
    IDLE_ANIM_DELAY = 5
    MOVING_ANIM_DELAY = 2
    IDLE_VELOCITY_THRESHOLD = 0.1
    images = Entity.load_images([
        'res/santa_back_down.png',
        'res/santa_back_up.png',
        # 'res/santa_front_down.png',
        # 'res/santa_front_up.png',
    ], scale_2x=True)

    def __init__(self, x, y, pos_bounds, is_turn=False):
        Player.__init__(self, x, y, self.images, pos_bounds=pos_bounds, is_turn=is_turn)
        self.anim_clock = 0
        self.anim_delay = Santa.IDLE_ANIM_DELAY

    def update(self, pressed_keys):
        Player.update(self, pressed_keys)
        if abs(self.xv) < Santa.IDLE_VELOCITY_THRESHOLD and abs(self.yv) < Santa.IDLE_VELOCITY_THRESHOLD:
            self.anim_delay = Santa.IDLE_ANIM_DELAY
        else:
            self.anim_delay = Santa.MOVING_ANIM_DELAY

        if self.anim_clock >= self.anim_delay:
            self.img_idx = (self.img_idx + 1) % len(self.images)
            self.image = self.images[self.img_idx]
            self.anim_clock = 0
        self.anim_clock += 1
