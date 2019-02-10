from collections import deque, namedtuple

import pygame as pg


# Components with Data

class PositionComp:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class VelocityComp:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MoveSpeedComp:
    def __init__(self, speed):
        self.speed = speed

SizeComp = namedtuple('SizeComp', ['w', 'h'])

class LifetimeComp:
    def __init__(self, life):
        self.life = life

class AmmoComp:
    def __init__(self):
        self.rounds = deque()

OwnerComp = namedtuple('OwnerComp', ['owner'])

InputConfigComp = namedtuple('InputConfigComp', ['key_map'])

class PlayerComp:
    MAX_HEALTH = 10
    MAX_POWER = 10
    MAX_DRUNKENNESS = 10

    def __init__(self, name, quotes, moves, mug_sprites, autonomous=False):
        self.curr_health = PlayerComp.MAX_HEALTH
        self.max_health = PlayerComp.MAX_HEALTH
        self.curr_power = 0
        self.max_power = PlayerComp.MAX_POWER
        self.curr_drunkenness = 0
        self.max_drunkenness = PlayerComp.MAX_DRUNKENNESS
        self.name = name
        self.quotes = quotes
        self.moves = moves
        self.mug_sprites = mug_sprites
        self.autonomous = autonomous
        self.opponent_name = None

class PositionBoundComp(pg.Rect): pass

PositionBoundBounceMultiplierComp = namedtuple(
                        'PositionBoundBounceMultiplierComp',
                        ['multiplier'])

class OutOfBoundsComp(pg.Rect): pass

class DrawComp(pg.sprite.Sprite):
    def __init__(self, images):
        pg.sprite.Sprite.__init__(self, self.groups)
        if not isinstance(images, list):
            images = [images]
        self.images = images
        self.img_idx = 0
        self.image = self.images[self.img_idx]
        self.rect = self.image.get_rect()

class AnimateComp:
    def __init__(self, delay=1.0):
        self.clock = 0
        self.delay = delay

SnowTargetComp = namedtuple('SnowTargetComp', ['x', 'y'])

class MemoryComp:
    def __init__(self, memory=dict()):
        self.memory = memory

# Flags

class CollideFlag: pass

class ProjectileFlag: pass

class BenjaminFlag: pass

class LoganFlag: pass

class LucasFlag: pass

class RobertFlag: pass

class DeAnneFlag: pass

class JoshuaFlag: pass

class JanicolousFlag: pass

class SantaFlag: pass

class TopPlayerFlag: pass

class BottomPlayerFlag: pass

class VelocityAttenuateFlag: pass

class OutOfBoundsKillFlag: pass

class DeadFlag: pass

