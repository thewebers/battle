import pygame as pg
from pygame.locals import *

from .entity import Entity
from .component import *


class Player:
    @staticmethod
    def init(entity, x, y, pos_bounds, sprites):
        entity.add_comp(PositionComp(x, y))
        entity.add_comp(VelocityComp(0.0, 0.0))
        entity.add_comp(PlayerComp())
        entity.add_comp(PositionBoundComp(pos_bounds))
        entity.add_comp(DrawComp(sprites))
        entity.add_comp(AnimateComp())
        # TODO: Make sure all sprites have the same dimensions.
        entity.add_comp(SizeComp(sprites[0].get_width(),
                                 sprites[0].get_height()))
