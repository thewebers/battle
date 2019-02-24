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


def _init_ball_chin_move(player):
    for _ in range(3):
        player.force_get_comp(AmmoComp).rounds.append(BallsProjectile)

def _init_chad_tosser_move(player):
    player.force_get_comp(AmmoComp).rounds.append(FootballProjectile)

def _init_the_joint_move(player):
    player.force_get_comp(AmmoComp).rounds.append(JointProjectile)


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
        'I don\'t have to workout for my muscles. Look at me!',
        'Butthead-fweak!!',
        'I can get away with whatever I want because mom and dad were also the youngest child. WEEEEEEEE!',
    ]
    MOVES = [
        MoveOption('BALL CHIN', 'A projectile of his ball chin.', _init_ball_chin_move),
        MoveOption('CHAD TOSSER', 'A big ole football because this guy IS GOOD AT SPORTS.', _init_chad_tosser_move),
        MoveOption('THE JOINT', 'Devil\'s Lettuce is especially devilish today.', _init_the_joint_move),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Benjamin.SPRITES,
                    Benjamin.NAME, Benjamin.QUOTES, Benjamin.MOVES,
                    Benjamin.MUG_SPRITES)
        entity.add_comp(TopPlayerComp())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(BenjaminFlag())
