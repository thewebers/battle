import pygame as pg

class Entity(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y

    @staticmethod
    def load_images(img_locs):
        """Loads and scales the images found in `img_locs`."""
        return [pg.image.load(img_loc) for img_loc in img_locs]
