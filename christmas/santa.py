import pygame as pg

from .entity import Entity
from .player import Player

# TODO: Make Santa a bot.

class Santa(Player):
    images = Entity.load_images(['res/santa.png'])

    def __init__(self, x, y, pos_bounds, is_turn=False):
        Player.__init__(self, x, y, self.images, pos_bounds=pos_bounds, is_turn=is_turn)

    def update(self, pressed_keys):
        Player.update(self, pressed_keys)
        self.img_idx = (self.img_idx + 1) % len(self.images)
        self.image = self.images[self.img_idx]
