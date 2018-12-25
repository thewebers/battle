import pygame as pg

from .component import *
from .entity import Entity
from .image import load_images
from .player import Player


class Benjamin:
    SPRITES = load_images([
        'res/img/ben_1.png',
        'res/img/ben_2.png'
    ], scale_factor=4)

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Benjamin.SPRITES)
        entity.add_comp(HumanFlagComp())


class BenjaminMug:
    ANIM_DELAY = 10
    SPRITES = load_images([
        'res/img/ben_mug_1.png',
        'res/img/ben_mug_2.png'
    ], scale_factor=4)

    @staticmethod
    def init(entity, x, y):
        entity.add_comp(PositionComp(x, y))
        entity.add_comp(DrawComp(BenjaminMug.SPRITES))
        entity.add_comp(AnimateComp(BenjaminMug.ANIM_DELAY))
