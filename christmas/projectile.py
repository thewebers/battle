import pygame as pg

from .component import *
from .image import load_images


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
