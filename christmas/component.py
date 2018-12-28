from collections import namedtuple

import pygame as pg

class PositionComp:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class VelocityComp:
    def __init__(self, x, y):
        self.x = x
        self.y = y

SizeComp = namedtuple('SizeComp', ['w', 'h'])

class LifetimeComp:
    def __init__(self, life):
        self.life = life

class PlayerComp:
    MAX_HEALTH = 10
    MAX_POWER = 10
    MAX_DRUNKENNESS = 10

    def __init__(self):
        self.curr_health = PlayerComp.MAX_HEALTH
        self.max_health = PlayerComp.MAX_HEALTH
        self.curr_power = 0
        self.max_power = PlayerComp.MAX_POWER
        self.curr_drunkenness = 0
        self.max_drunkenness = PlayerComp.MAX_DRUNKENNESS

class PositionBoundComp(pg.Rect): pass

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
    def __init__(self, delay):
        self.clock = 0
        self.delay = delay

class TurnFlagComp: pass

class WeberFlagComp: pass

class SantaFlagComp: pass

class VelocityAttenuateFlagComp: pass

class DeadFlagComp: pass

class SnowFlagComp: 
    def __init__(self, x, y):
        self.x = x
        self.y = y