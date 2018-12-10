
import pygame as pg

from .player import Player

# TODO: Make Santa a bot

class Santa(Player):

    images = list(map(pg.image.load, ['res/santa_1.bmp', 'res/santa_2.bmp']))

    def __init__(self, x, y, region, is_turn=False):
        Player.__init__(self, x, y, self.images, bounded_region=region, is_turn=is_turn)
        print('Santa, created')

    def update(self, pressed_keys):
        Player.update(self, pressed_keys)
        self.img_idx = (self.img_idx + 1) % len(self.images)
        self.image = self.images[self.img_idx]
        print('Santa, updated')