import pygame as pg


class DrawRect(pg.Rect):
    """PyGame `Rect` that can be drawn."""
    def draw(self, screen, color):
        pg.draw.rect(screen, color, self)

