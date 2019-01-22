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
from .projectile import RockPileProjectile, GiftOfLifeProjectile, MrSpoonProjectile


def _init_its_clobberin_time(player):
    for _ in range(3):
        player.force_get_comp(AmmoComp).rounds.append(RockPileProjectile)

def _init_the_gift_of_life_move(player):
    player.force_get_comp(AmmoComp).rounds.append(GiftOfLifeProjectile)

def _init_next_week_move(player):
    player.force_get_comp(AmmoComp).rounds.append(MrSpoonProjectile)


class DeAnne:
    SPRITES = load_images([
        'res/img/dee_1.png',
        'res/img/dee_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_SPRITES = load_images([
        'res/img/dee_mug_1.png',
        'res/img/dee_mug_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_ANIM_DELAY = 10
    NAME = 'DeAnne'
    QUOTES = [
        'Imma knock you into next week!',
        'What the hell?',
        'Really? Really. You\'re gonna do that.',
        'Well you\'re as useless as tits on a boar.',
    ]
    MOVES = [
        MoveOption('IT\'S CLOBBERIN\' TIME', 'Mommy finds big rock and is looking at you in an alarming way.', _init_its_clobberin_time),
        MoveOption('THE GIFT OF LIFE', 'Creates another testosterone-filled Weber.', _init_the_gift_of_life_move),
        MoveOption('NEXT WEEK', 'Imma knock you into next week. Only this time, I mean it.', _init_next_week_move),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, DeAnne.SPRITES,
                    DeAnne.NAME, DeAnne.QUOTES, DeAnne.MOVES,
                    DeAnne.MUG_SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(DeAnneFlag())