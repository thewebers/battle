import numpy as np
import random

import pygame as pg

from .component import *
from .util import DrawRect, make_color_surface


class Perlin:
    '''Generate a 2-D Perlin distribution.

    More information: https://www.scratchapixel.com/lessons/procedural-generation-virtual-worlds/perlin-noise-part-2
    '''
    SEED_MAX = 15

    def generate(w, h, n, thresh=0.5):
        # TODO: Argument documentation.
        # TODO: Use arguments.
        lin1 = np.linspace(0, w, n, endpoint=False)
        lin2 = np.linspace(0, h, n, endpoint=False)
        x, y = np.meshgrid(lin1, lin2)
        # lin = np.linspace(0, 5, 100, endpoint=False)
        # x, y = np.meshgrid(lin, lin)
        grid = Perlin._perlin(x, y, seed=random.randint(0, Perlin.SEED_MAX))
        return grid

    @staticmethod
    def _perlin(x, y, seed=0):
        # Permutation Table
        np.random.seed(seed)
        p = np.arange(256, dtype=int)
        np.random.shuffle(p)
        p = np.stack([p, p]).flatten()
        # Coordinates of the Top-left
        xi = x.astype(int)
        yi = y.astype(int)
        # Internal Coordinates
        xf = x - xi
        yf = y - yi
        # Fade Factors
        u = Perlin._fade(xf)
        v = Perlin._fade(yf)
        # Noise Components
        n00 = Perlin._gradient(p[p[xi] + yi], xf, yf)
        n01 = Perlin._gradient(p[p[xi] + yi + 1], xf, yf - 1)
        n11 = Perlin._gradient(p[p[xi + 1] + yi + 1], xf -1, yf-1)
        n10 = Perlin._gradient(p[p[xi + 1] + yi], xf - 1, yf)
        # Combine noises.
        x1 = Perlin._lerp(n00, n10, u)
        x2 = Perlin._lerp(n01, n11, u)
        return Perlin._lerp(x1,x2,v)

    @staticmethod
    def _lerp(a, b, x):
        """Performs 'LinEar inteRPolation'."""
        return a + x * (b - a)

    @staticmethod
    def _fade(t):
        """Performs 6t^5 - 15t^4 + 10t^3"""
        return 6 * t**5 - 15 * t**4 + 10 * t**3

    @staticmethod
    def _gradient(h, x, y):
        """Grad converts `h` to the right gradient vector and return the dot product with `(x,y)`."""
        vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        g = vectors[h % 4]
        return g[:, :, 0] * x + g[:, :, 1] * y


class SnowGlobe:
    COLORS = [(255,) * 3, (220,) * 3]
    DIMEN  = (4,) * 2
    OOB_PADDING = 50 # px

    def __init__(self, w, h, create_entitiy, debug_mode=False):
        self.w = w
        self.h = h
        self.create_entitiy = create_entitiy
        # Generate initial snow from Perlin distribution.
        # TODO: Generate absolute True/False grid with correct screen dimensions and pixel density.
        # TODO: Generate snow from grid.
        if debug_mode:
            return
        grid = Perlin.generate(20, 40, 50)

    @staticmethod
    def create_snowflake():
        return make_color_surface(SnowGlobe.DIMEN, random.choice(SnowGlobe.COLORS))

    def shake(self):
        """Spawn snow entities."""
        t = pg.time.get_ticks()

        if t % 1000 != 0:
            return

        x, y = (random.randint(0, self.w + 1), 0)
        target_x, target_y = (x, random.randint(0, self.h + 1))
        sprites = [self.create_snowflake()]
        bounds = DrawRect(-SnowGlobe.OOB_PADDING, -SnowGlobe.OOB_PADDING, \
                          self.w + SnowGlobe.OOB_PADDING, self.h + SnowGlobe.OOB_PADDING, (0, 0, 0))

        # Create entity with components.
        entity = self.create_entitiy()
        entity.add_comp(PositionComp(x, y))
        entity.add_comp(VelocityComp(0.0, 1.0))
        entity.add_comp(SizeComp(*SnowGlobe.DIMEN))
        entity.add_comp(OutOfBoundsComp(bounds))
        entity.add_comp(SnowTargetComp(target_x, target_y))
        entity.add_comp(DrawComp(sprites))
