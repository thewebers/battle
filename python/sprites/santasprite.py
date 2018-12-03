
import pygame as pg
from .blocksprite import BlockSprite

class SantaSprite(BlockSprite):
    def __init__(self):
        BlockSprite.__init__(self)
        self.timer = 0
    def get_surface(self):
        if self.timer % 2 == 0:
            myimage = pg.image.load('res/santa_1.bmp')
        else:
            myimage = pg.image.load('res/santa_2.bmp')
        return myimage
    def update(self):
        pass