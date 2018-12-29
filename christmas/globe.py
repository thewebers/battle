import pygame as pg

import random

from .component import *
from .util import DrawRect


class SnowGlobe:
    COLORS = [(255,) * 3, (220,) * 3] 
    DIMEN  = (2,) * 2
    OOB_PADDING = 50 # px

    def __init__(self, w, h, create_entitiy):
        self.w = w
        self.h = h
        self.create_entitiy = create_entitiy

    @staticmethod
    def create_snowflake():
        flake = pg.Surface(SnowGlobe.DIMEN)
        flake.fill(random.choice(SnowGlobe.COLORS))
        return flake

    def shake(self):
        """Spawn snow entities."""
        t = pg.time.get_ticks()

        if t % 1000 != 0:
            return
        
        x, y = (random.randint(0, self.w + 1), 0)
        target_x, target_y = (x, random.randint(0, self.h + 1))
        sprites = [self.create_snowflake()]
        bounds = DrawRect(-SnowGlobe.OOB_PADDING, -SnowGlobe.OOB_PADDING, \
                          self.w + SnowGlobe.OOB_PADDING, self.h + SnowGlobe.OOB_PADDING)

        # Create entity with components.
        entity = self.create_entitiy()
        entity.add_comp(PositionComp(x, y))
        entity.add_comp(VelocityComp(0.0, 1.0))
        entity.add_comp(SizeComp(*SnowGlobe.DIMEN))
        entity.add_comp(OutOfBoundsComp(bounds))
        entity.add_comp(ParticleComp(target_x, target_y))
        entity.add_comp(DrawComp(sprites))