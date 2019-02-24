from enum import Enum

import pygame as pg
from pygame.locals import *

from .component import *
from .dialog import DialogFrame
from .entity import Entity
from .image import load_images
from .input_handler import BOTTOM_PLAYER_INPUT_CONFIG
from .player import Player, MoveOption
from .projectile import CoalProjectile, BeerProjectile, ElfProjectile


# TODO: Projectiles.


def _init_coal_move(player):
    for _ in range(3):
        player.force_get_comp(AmmoComp).rounds.append(CoalProjectile)


def _init_beer_move(player):
    for _ in range(2):
        player.force_get_comp(AmmoComp).rounds.append(BeerProjectile)


def _init_elf_move(player):
    player.force_get_comp(AmmoComp).rounds.append(ElfProjectile)


class Santa:
    SPRITES = load_images([
        'res/img/santa_back_1.png',
        'res/img/santa_back_2.png',
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
    ]
    MOVES = [
        MoveOption('Coal', 'Coal in yo a-hole', _init_coal_move),
        MoveOption('Beer', 'Get fukn turnt, kids', _init_beer_move),
        MoveOption('Elf', 'DAD! DYAAADDDD!!!!', _init_elf_move),
    ]
    STARTING_DRUNKENNESS = 5

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Santa.SPRITES,
                    Santa.NAME, Santa.QUOTES, Santa.MOVES,
                    Santa.MUG_SPRITES)
        entity.add_comp(ParticleSourceComp('drunk',
                                           Santa.STARTING_DRUNKENNESS))
        entity.add_comp(BottomPlayerComp())
        entity.add_comp(InputConfigComp(BOTTOM_PLAYER_INPUT_CONFIG))
        entity.add_comp(SantaFlag())
        entity.add_comp(AutoComp('manhattan'))
