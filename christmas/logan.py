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


class Logan:
    SPRITES = load_images([
        'res/img/logan_1.png',
        'res/img/logan_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_SPRITES = load_images([
        'res/img/logan_mug_1.png',
        'res/img/logan_mug_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_ANIM_DELAY = 10
    QUOTES = [
        'Eat carpel toobley!',
        'I\'m very ready to zonk right about now. Zzzzz.',
    ]
    MOVES = [
        MoveOption('[B]alls', 'A projectile of BALLS'),
        MoveOption('[C]had Toss', 'A big ole football'),
        MoveOption('Balls [T]wo', 'A projectile of BALLS (part two)'),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Logan.SPRITES,
                    Logan.NAME, Logan.QUOTES, Logan.MOVES,
                    Logan.MUG_SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(LoganFlag())