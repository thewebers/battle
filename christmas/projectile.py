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
    SPRITES = load_images(['res/img/balls.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        BallsProjectile.SPRITES, BallsProjectile.LIFETIME)


class FootballProjectile:
    SPRITES = load_images(['res/img/football.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        FootballProjectile.SPRITES, FootballProjectile.LIFETIME)


class JointProjectile:
    SPRITES = load_images(['res/img/joint.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv, JointProjectile.SPRITES, JointProjectile.LIFETIME)


class DumbbellProjectile:
    SPRITES = load_images(['res/img/dumbbell.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        DumbbellProjectile.SPRITES, DumbbellProjectile.LIFETIME)


class FinancialReportProjectile:
    SPRITES = load_images(['res/img/financial_report.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        FinancialReportProjectile.SPRITES, FinancialReportProjectile.LIFETIME)


class HayBaleProjectile:
    SPRITES = load_images(['res/img/hay.png'], scale_factor=2)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        HayBaleProjectile.SPRITES, HayBaleProjectile.LIFETIME)


class RockPileProjectile:
    SPRITES = load_images(['res/img/rock_pile.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        RockPileProjectile.SPRITES, RockPileProjectile.LIFETIME)


class GiftOfLifeProjectile:
    SPRITES = load_images(['res/img/gift_of_life.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        GiftOfLifeProjectile.SPRITES, GiftOfLifeProjectile.LIFETIME)


class MrSpoonProjectile:
    SPRITES = load_images(['res/img/mr_spoon.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        MrSpoonProjectile.SPRITES, MrSpoonProjectile.LIFETIME)


class BreakdanceTornadoProjectile:
    SPRITES = load_images(['res/img/breakdance_tornado.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        BreakdanceTornadoProjectile.SPRITES, BreakdanceTornadoProjectile.LIFETIME)


class SilentNightProjectile:
    SPRITES = load_images(['res/img/silent_night.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        SilentNightProjectile.SPRITES, SilentNightProjectile.LIFETIME)


class GrayEyebrowProjectile:
    SPRITES = load_images(['res/img/gray_eyebrow.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        GrayEyebrowProjectile.SPRITES, GrayEyebrowProjectile.LIFETIME)


class LubeTubeProjectile:
    SPRITES = load_images(['res/img/lube.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        LubeTubeProjectile.SPRITES, LubeTubeProjectile.LIFETIME)


class ProteinShakeProjectile:
    SPRITES = load_images(['res/img/protein_shake.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        ProteinShakeProjectile.SPRITES, ProteinShakeProjectile.LIFETIME)


class RobotProjectile:
    SPRITES = load_images(['res/img/robot.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        RobotProjectile.SPRITES, RobotProjectile.LIFETIME)


class FiveGProjectile:
    SPRITES = load_images(['res/img/5g.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        FiveGProjectile.SPRITES, FiveGProjectile.LIFETIME)


class LiteratureProjectile:
    SPRITES = load_images(['res/img/literature.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        LiteratureProjectile.SPRITES, LiteratureProjectile.LIFETIME)


class SemenProjectile:
    SPRITES = load_images(['res/img/cum.png'], scale_factor=4)
    LIFETIME = 60

    @staticmethod
    def init(entity, owner, x, y, xv, yv):
        Projectile.init(entity, owner, x, y, xv, yv,
                        SemenProjectile.SPRITES, SemenProjectile.LIFETIME)