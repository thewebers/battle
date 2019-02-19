from .component import *
from .image import load_images
from .player import Player


class Particle:
    def init():
        pass


class BubbleParticle(Particle):
    SPRITES = load_images(['res/img/bubble_1.png',
                           'res/img/bubble_2.png'], scale_factor=4)
    LIFETIME = 20
    DEFAULT_ANIM_DELAY = 5
    @staticmethod
    def init(entity, pos):
        entity.add_comp(PositionComp(*pos))
        entity.add_comp(DrawComp(BubbleParticle.SPRITES))
        entity.add_comp(AnimateComp(BubbleParticle.DEFAULT_ANIM_DELAY))
        entity.add_comp(SizeComp(BubbleParticle.SPRITES[0].get_width(),
                                 BubbleParticle.SPRITES[0].get_height()))
        entity.add_comp(LifetimeComp(BubbleParticle.LIFETIME))