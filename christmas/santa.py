import pygame as pg

from .component import *
from .entity import Entity
from .image import load_images
from .player import Player


class Santa:
    SPRITES = load_images([
        'res/img/santa_back_1.png',
        'res/img/santa_back_2.png',
        # 'res/santa_front_down.png',
        # 'res/santa_front_up.png',
    ], scale_factor=4)

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Santa.SPRITES)
        entity.add_comp(SantaFlagComp())


class SantaMug:
    ANIM_DELAY = 10
    SPRITES = load_images([
        'res/img/santa_mug_1.png',
        'res/img/santa_mug_2.png'
    ], scale_factor=4)

    @staticmethod
    def init(entity, x, y):
        entity.add_comp(PositionComp(x, y))
        entity.add_comp(DrawComp(SantaMug.SPRITES))
        entity.add_comp(AnimateComp(SantaMug.ANIM_DELAY))
