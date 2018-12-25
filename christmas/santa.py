import pygame as pg

from .component import *
from .entity import Entity
from .image import load_images
from .player import Player

# TODO: Make Santa a bot.

class Santa:
    SPRITES = load_images([
        'res/santa_back_down.png',
        'res/santa_back_up.png',
        # 'res/santa_front_down.png',
        # 'res/santa_front_up.png',
    ], scale_factor=4)

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Santa.SPRITES)
        entity.add_comp(SantaFlagComp())
