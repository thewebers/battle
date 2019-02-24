from collections import namedtuple

import pygame as pg
from pygame.locals import *

from .entity import Entity
from .component import *


class Player:
    DEFAULT_ANIM_DELAY = 5
    BOUNCE_MULTIPLIER = 8.0
    MOVE_SPEED = 7.0
    SPRITE_SCALE_FACTOR = 4

    @staticmethod
    def init(entity, x, y, pos_bounds, sprites, name, quotes, moves, \
             mug_sprites):
        entity.add_comp(PositionComp(x, y))
        entity.add_comp(VelocityComp(0.0, 0.0))
        entity.add_comp(MoveSpeedComp(Player.MOVE_SPEED))
        entity.add_comp(PlayerComp(name, quotes, moves, mug_sprites))
        entity.add_comp(PositionBoundComp(pos_bounds))
        entity.add_comp(PositionBoundBounceMultiplierComp( \
                                                    Player.BOUNCE_MULTIPLIER))
        entity.add_comp(DrawComp(sprites))
        entity.add_comp(AnimateComp(Player.DEFAULT_ANIM_DELAY))
        entity.add_comp(SizeComp(sprites[0].get_width(),
                                 sprites[0].get_height()))
        entity.add_comp(VelocityAttenuateFlag())
        entity.add_comp(CollideFlag())
        entity.add_comp(MemoryComp())


MoveOption = namedtuple('MoveOption', ['prompt', 'description', 'move_init'])
