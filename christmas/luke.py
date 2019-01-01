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
from .projectile import BallsProjectile, FootballProjectile, JointProjectile


def _init_lube_tube_move(player):
    for _ in range(3):
        player.force_get_comp(AmmoComp).rounds.append(BallsProjectile)

def _init_protein_shake_move(player):
    player.force_get_comp(AmmoComp).rounds.append(FootballProjectile)

def _init_robot_move(player):
    player.force_get_comp(AmmoComp).rounds.append(JointProjectile)


class Lucas:
    SPRITES = load_images([
        'res/img/luke_1.png',
        'res/img/luke_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_SPRITES = load_images([
        'res/img/luke_mug_1.png',
        'res/img/luke_mug_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_ANIM_DELAY = 10
    NAME = 'Lucas'
    QUOTES = [
        '...and that\'s the way it was.',
        'Yeah dude, the thing about the human brain is...',
        'I do much enjoy intercourse.',
        'I have a box of every Yu-Gi-Oh card on the planet, but we can\'t find it...',
        'Did you know I have a science lab right under my bed? Sorry, it only opens for me.',
    ]
    MOVES = [
        MoveOption('LUBE TUBE', 'A bottle of canola oil saved for this very occasion.', _init_lube_tube_move),
        MoveOption('PROTEIN SHAKE', 'A concoction for massive gains.', _init_protein_shake_move),
        MoveOption('ROBOT', 'Little slave robot come after you hard.', _init_robot_move),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Lucas.SPRITES,
                    Lucas.NAME, Lucas.QUOTES, Lucas.MOVES,
                    Lucas.MUG_SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(LucasFlag())