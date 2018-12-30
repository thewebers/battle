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
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_SPRITES = load_images([
        'res/img/ben_mug_1.png',
        'res/img/ben_mug_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_ANIM_DELAY = 10
    NAME = 'Benjamin'
    QUOTES = [
        'Eat balls!',
    ]
    MOVES = [
        MoveOption('BALL CHIN', 'A projectile of his ball chin.'),
        MoveOption('CHAD TOSSER', 'A big ole football'),
        MoveOption('JOINT', 'Devil\'s Lettuce is especially devilish.'),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Benjamin.SPRITES,
                    Benjamin.NAME, Benjamin.QUOTES, Benjamin.MOVES,
                    Benjamin.MUG_SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(BenjaminFlag())
