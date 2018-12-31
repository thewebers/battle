import pygame as pg


class DrawRect(pg.Rect):
    """PyGame `Rect` that can be drawn."""

    def __init__(self, x, y, w, h, color):
        super(DrawRect, self).__init__(x, y, w, h)
        self.color = color

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self)


def make_color_surface(dimensions, color):
    result = pg.Surface(dimensions)
    result.fill(color)
    return result
