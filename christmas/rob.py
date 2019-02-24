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
from .projectile import DumbbellProjectile, FinancialReportProjectile, HayBaleProjectile


def _init_dad_strength_move(player):
    for _ in range(3):
        player.force_get_comp(AmmoComp).rounds.append(DumbbellProjectile)

def _init_financial_report_move(player):
    player.force_get_comp(AmmoComp).rounds.append(FinancialReportProjectile)

def _init_hay_bale_move(player):
    player.force_get_comp(AmmoComp).rounds.append(HayBaleProjectile)


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
        MoveOption('DAD STRENGTH', 'A 50 lbs dumbbell for your face to consume.', _init_dad_strength_move),
        MoveOption('FINANCIAL REPORT', 'A financial report tailored just for you.', _init_financial_report_move),
        MoveOption('HAY BALE', 'The devil went down to Georgia.', _init_hay_bale_move),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Robert.SPRITES,
                    Robert.NAME, Robert.QUOTES, Robert.MOVES,
                    Robert.MUG_SPRITES)
        entity.add_comp(TopPlayerComp())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(RobertFlag())