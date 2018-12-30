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


class DeAnne:
    SPRITES = load_images([
        'res/img/luke_1.png',
        'res/img/luke_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_SPRITES = load_images([
        'res/img/luke_mug_1.png',
        'res/img/luke_mug_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_ANIM_DELAY = 10
    QUOTES = [
        '...and that\'s the way it was.',
    ]
    MOVES = [
        MoveOption('LUBE TUBE', 'A bottle of canola oil saved for this very occasion.'),
        MoveOption('PROTEIN SHAKE', 'A concoction for massive gains.'),
        MoveOption('ROBOT', 'Little slave robot come after you hard.'),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Logan.SPRITES,
                    Logan.NAME, Logan.QUOTES, Logan.MOVES,
                    Logan.MUG_SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(LoganFlag())