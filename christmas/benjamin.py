from enum import Enum

import pygame as pg
from pygame.locals import *

from .color import *
from .component import *
from .dialog import DialogFrame
from .entity import Entity
from .image import load_images
from .player import Player, MoveOption
from .santa import CoalProjectile


class Benjamin:
    SPRITES = load_images([
        'res/img/ben_1.png',
        'res/img/ben_2.png'
    ], scale_factor=4)
    MUG_SPRITES = load_images([
        'res/img/ben_mug_1.png',
        'res/img/ben_mug_2.png'
    ], scale_factor=4)
    MUG_ANIM_DELAY = 10
    QUOTES = [
        'Eat balls!',
    ]
    MOVES = [
        MoveOption('[B]alls', K_b),
        MoveOption('[C]had Toss', K_c),
        MoveOption('Balls [T]wo', K_t),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Benjamin.SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(BenjaminFlag())
        entity.add_comp(MugComp(Benjamin.MUG_SPRITES))
        entity.add_comp(QuoteComp(Benjamin.QUOTES))
        entity.add_comp(MoveSelectComp(Benjamin.MOVES))
