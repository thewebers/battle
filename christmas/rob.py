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


class Robert:
    SPRITES = load_images([
        'res/img/rob_1.png',
        'res/img/rob_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_SPRITES = load_images([
        'res/img/rob_mug_1.png',
        'res/img/rob_mug_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_ANIM_DELAY = 10
    NAME = 'Robert'
    QUOTES = [
        'Are you FRICKIN\' kiddin\' me?.',
        'Jimminy Christmas!',
        'HUH?',
        'Seriously? No, seriously?',
        'WHAT\'S THAT?',
        'Life is simple economics. Human desires are insatiable.',
        'Hindsight is 20/20.'
    ]
    MOVES = [
        MoveOption('DAD STRENGTH', 'A 50 lbs dumbbell for your face to consume.'),
        MoveOption('FINANCIAL REPORT', 'A financial report tailored just for you.'),
        MoveOption('HAY BALE', 'The devil went down to Georgia.'),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Robert.SPRITES,
                    Robert.NAME, Robert.QUOTES, Robert.MOVES,
                    Robert.MUG_SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(RobertFlag())