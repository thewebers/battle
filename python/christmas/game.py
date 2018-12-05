import random

import pygame as pg
from pygame.locals import *

from .player import Player

FPS = 30

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Game:
    """Handles all game logic and interfaces with UI via pygame."""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def start(self):
        """Let the sin... begin."""
        self.init()
        self.loop()

    def init(self):
        pg.init()
        # Sound
        pg.mixer.init()

        # Window
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption('Another Ordinary Weber Christmas')
        # We don't use no motherfucking mouse.
        pg.mouse.set_visible(False)

        self.clock = pg.time.Clock()

        # Images
        Player.images = list(map(pg.image.load, ['res/santa_1.bmp', 'res/santa_2.bmp']))
        self.groups = {
            'all': pg.sprite.RenderUpdates(),
        }

        Player.groups = self.groups['all']

        self.player = Player(self.width // 2, self.height // 2)

    def loop(self):
        running = True
        while running:
            # Poll the events.
            for event in pg.event.get():
                # Check if they tryna leave.
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False
            pressed_keys = pg.key.get_pressed()

            # Update sprites.
            self.groups['all'].update(pressed_keys)

            # Draw/render.
            self.screen.fill(WHITE)

            # myfont = pg.font.SysFont("Comic Sans MS", 30)
            # # apply it to text on a label
            # label = myfont.render("teeny weeny in ben's tummy", 1, BLACK)
            # # put the label object on the self.screen at point x=100, y=100
            # self.screen.blit(label, (20, 100))

            self.groups['all'].draw(self.screen)

            # Send results to screen.
            pg.display.flip()

            # Will make the loop run at the same speed all the time.
            self.clock.tick(FPS)

        pg.quit()
