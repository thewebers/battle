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
    NAME = 'Benjamin'
    QUOTES = [
        'Eat balls!',
    ]
    MOVES = [
        MoveOption('Balls', 'A projectile of BALLS'),
        MoveOption('Chad Toss', 'A big ole football'),
        MoveOption('Balls Two', 'A projectile of BALLS (part two)'),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Benjamin.SPRITES,
                    Benjamin.NAME, Benjamin.QUOTES, Benjamin.MOVES,
                    Benjamin.MUG_SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(BenjaminFlag())
