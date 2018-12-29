from enum import Enum

import pygame as pg
from pygame.locals import *

from .color import *
from .component import *
from .dialog import DialogFrame
from .entity import Entity
from .image import load_images
from .input_handler import TOP_PLAYER_INPUT_CONFIG
from .player import Player, MoveOption


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
        MoveOption('[B]alls', K_b, 'A projectile of BALLS'),
        MoveOption('[C]had Toss', K_c, 'A big ole football'),
        MoveOption('Balls [T]wo', K_t, 'A projectile of BALLS (part two)'),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Benjamin.SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(BenjaminFlag())
        entity.add_comp(MugComp(Benjamin.MUG_SPRITES))
        entity.add_comp(QuoteComp(Benjamin.QUOTES))
        entity.add_comp(MoveSelectComp(Benjamin.MOVES))
