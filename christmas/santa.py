from enum import Enum

import pygame as pg
from pygame.locals import *

from .component import *
from .dialog import DialogFrame
from .entity import Entity
from .image import load_images
from .input_handler import BOTTOM_PLAYER_INPUT_CONFIG
from .player import Player, MoveOption


class Santa:
    SPRITES = load_images([
        'res/img/santa_back_1.png',
        'res/img/santa_back_2.png',
        # 'res/santa_front_down.png',
        # 'res/santa_front_up.png',
    ], scale_factor=4)
    MUG_ANIM_DELAY = 10
    MUG_SPRITES = load_images([
        'res/img/santa_mug_1.png',
        'res/img/santa_mug_2.png'
    ], scale_factor=4)
    NAME = 'Santa'
    QUOTES = [
        'Get ready for some hot suck of dick!',
        'Hey, you came here to fight!',
        'What are you wearing? \'Cause it looks like something you\'re ready to fight in.',
        'How far have you gotten with a man who\'s in his mid-40s?',
        'On an unrelated note, I\'m 44.',
        'Woah. I sure can take a punch.',
        'That all? I wish... it was.',
        'Yeah sure, spill blood all over my HAND-CRAFTED SUIT?! COME ON!',
        # TODO: The ones below are actually Luke's.
        'Can we smoke a little weed?  My words get better.',
        'When considering intelligence, you can be a retarded professional and still be retarded.'
    ]
    MOVES = [
        MoveOption('Coal', 'Coal in yo a-hole'),
        MoveOption('Beer', 'Get fukn turnt, kids'),
        MoveOption('Rudolph', 'Eat red nose, nerd'),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Santa.SPRITES,
                    Santa.NAME, Santa.QUOTES, Santa.MOVES,
                    Santa.MUG_SPRITES)
        entity.add_comp(BottomPlayerFlag())
        entity.add_comp(InputConfigComp(BOTTOM_PLAYER_INPUT_CONFIG))
        entity.add_comp(SantaFlag())
