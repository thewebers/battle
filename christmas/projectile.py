import pygame as pg

from .color import *
from .component import *
from .image import load_images
from .util import make_color_surface


class Projectile:
    BOUNCE_MULTIPLIER = 1

    def static_init(width, height):
        Projectile.POS_BOUND = pg.Rect(0, 0, width, height)

    def init(entity, owner, x, y, xv, yv, sprites, lifetime):
        entity.add_comp(PositionComp(x, y))
        entity.add_comp(VelocityComp(xv, yv))
        entity.add_comp(CollideFlag())
        entity.add_comp(ProjectileFlag())
        entity.add_comp(PositionBoundComp(Projectile.POS_BOUND))
        entity.add_comp(PositionBoundBounceMultiplierComp(Projectile.BOUNCE_MULTIPLIER))
        entity.add_comp(OwnerComp(owner))
        entity.add_comp(LifetimeComp(lifetime))
        entity.add_comp(DrawComp(sprites))
        entity.add_comp(SizeComp(sprites[0].get_width(),
                                 sprites[0].get_height()))


class CoalProjectile:
    SPRITES = load_images([
        'res/img/coal.png',
    ], scale_factor=4)
    LIFETIME = 90

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv, CoalProjectile.SPRITES, CoalProjectile.LIFETIME)


class BeerProjectile:
    SPRITES = [make_color_surface((80, 80), YELLOW)]
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        BeerProjectile.SPRITES, BeerProjectile.LIFETIME)


class ElfProjectile:
    SPRITES = [make_color_surface((100, 100), GREEN)]
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        ElfProjectile.SPRITES, ElfProjectile.LIFETIME)


class BallsProjectile:
    SPRITES = [make_color_surface((100, 100), ORANGE)]
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        BallsProjectile.SPRITES, BallsProjectile.LIFETIME)


class FootballProjectile:
    SPRITES = [make_color_surface((80, 140), RED)]
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        FootballProjectile.SPRITES, FootballProjectile.LIFETIME)


class JointProjectile:
    SPRITES = [make_color_surface((40, 40), GREEN)]
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv, JointProjectile.SPRITES, JointProjectile.SPRITES)


class DumbbellProjectile:
    SPRITES = load_images(['res/img/dumbbell.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        DumbbellProjectile.SPRITES, DumbbellProjectile.LIFETIME)
