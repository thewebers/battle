import random

import pygame as pg
from pygame.locals import *

from .player import Player
from .santa import Santa

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

        # Compute player regions and start positions.
        weber_region = ((0, 0), (self.width, self.height / 2))             # Top half
        santa_region = ((0, self.height / 2), (self.width, self.height))   # Bottom half
        weber_pos = ((weber_region[1][0] + weber_region[0][0]) / 2, (weber_region[1][1] + weber_region[0][1]) / 2)
        santa_pos = ((santa_region[1][0] + santa_region[0][0]) / 2, (santa_region[1][1] + santa_region[0][1]) / 2)

        # Initialize players
        # TODO: Loading menu
        self.groups = {
            'all': pg.sprite.RenderUpdates(),
        }
        Player.groups = self.groups['all']
        self.santa = Santa(santa_pos[0], santa_pos[1], santa_region, is_turn=True)
        self.weber = Santa(weber_pos[0], weber_pos[1], weber_region)

    def dialog(self, msg):
        myfont = pg.font.SysFont("Comic Sans MS", 30)
        dialog = myfont.render(msg.upper(), 1, BLACK)
        dialog_rect = dialog.get_rect(center=(self.width / 2, self.height / 2))
        self.screen.blit(dialog, dialog_rect)

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

            self.groups['all'].draw(self.screen)
            
            self.dialog(str((self.santa.x, self.santa.y)))

            # Send results to screen.
            pg.display.flip()

            # Will make the loop run at the same speed all the time.
            self.clock.tick(FPS)

        pg.quit()
