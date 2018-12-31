import pygame as pg

import random

from .component import *
from .util import make_color_surface


class SnowGlobe:
    COLORS = [(255,) * 3, (240,) * 3]
    DIMEN  = (4, 4)

    def __init__(self, w, h, create_entitiy):
        self.w = w
        self.h = h
        self.create_entitiy = create_entitiy

    @staticmethod
    def create_snowflake():
        return make_color_surface(SnowGlobe.DIMEN, random.choice(SnowGlobe.COLORS))

    def shake(self):
        """Spawn snow entities."""
        t = pg.time.get_ticks()

        # TODO: Correct and loop this, make more intense with greater t.

        x, y = (random.randint(0, self.w + 1), 0)
        target_x, target_y = (x, random.randint(0, self.h + 1))
        sprites = [self.create_snowflake()]
        pos_bounds = pg.Rect(0, 0, self.w, self.h)

        entity = self.create_entitiy()
        entity.add_comp(PositionComp(x, y))
        entity.add_comp(VelocityComp(0.0, 1.0))
        entity.add_comp(PositionBoundComp(pos_bounds))
        entity.add_comp(OutOfBoundsKillFlag())
        entity.add_comp(SnowTargetComp(target_x, target_y))
        entity.add_comp(DrawComp(sprites))
