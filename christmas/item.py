from .component import *
from .image import load_images
from .player import Player


class Item:
    def init():
        pass


class OrnamentItem(Item):
    SPRITES = load_images(['res/img/ornament_1.png'], scale_factor=4)
    LIFETIME = 500
    @staticmethod
    def init(entity, pos):
        entity.add_comp(PositionComp(*pos))
        entity.add_comp(DrawComp(OrnamentItem.SPRITES))
        entity.add_comp(AnimateComp(Player.DEFAULT_ANIM_DELAY))
        entity.add_comp(SizeComp(OrnamentItem.SPRITES[0].get_width(),
                                 OrnamentItem.SPRITES[0].get_height()))
        entity.add_comp(LifetimeComp(OrnamentItem.LIFETIME))
        entity.add_comp(CollideFlag())


class BeerItem(Item):
    SPRITES = load_images(['res/img/beer.png'], scale_factor=4)
    LIFETIME = 500
    @staticmethod
    def init(entity, pos):
        entity.add_comp(PositionComp(*pos))
        entity.add_comp(DrawComp(BeerItem.SPRITES))
        entity.add_comp(AnimateComp(Player.DEFAULT_ANIM_DELAY))
        entity.add_comp(SizeComp(BeerItem.SPRITES[0].get_width(),
                                 BeerItem.SPRITES[0].get_height()))
        entity.add_comp(LifetimeComp(BeerItem.LIFETIME))
        entity.add_comp(CollideFlag())