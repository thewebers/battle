from collections import namedtuple

import pygame as pg
from pygame.locals import *

from .entity import Entity
from .component import *


class Player:
    DEFAULT_ANIM_DELAY = 5

    @staticmethod
    def init(entity, x, y, pos_bounds, sprites):
        entity.add_comp(PositionComp(x, y))
        entity.add_comp(VelocityComp(0.0, 0.0))
        entity.add_comp(PlayerComp())
        entity.add_comp(PositionBoundComp(pos_bounds))
        entity.add_comp(DrawComp(sprites))
        entity.add_comp(AnimateComp(Player.DEFAULT_ANIM_DELAY))
        # TODO: Make sure all sprites have the same dimensions in the
        # `load_images` method.
        entity.add_comp(SizeComp(sprites[0].get_width(),
                                 sprites[0].get_height()))
        entity.add_comp(VelocityAttenuateFlag())


MoveOption = namedtuple('MoveOption', ['prompt', 'key', 'description'])
