import pygame as pg

from .component import *
from .entity import Entity
from .image import load_images
from .player import Player


class Benjamin:
    SPRITES = load_images(['res/benjamin.png'])

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Benjamin.SPRITES)
        entity.add_comp(HumanFlagComp())
