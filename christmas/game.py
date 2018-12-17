import random

import pygame as pg
from pygame.locals import *

from .player import Player
from .santa import Santa
from .benjamin import Benjamin

FPS = 30

# Define Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Game:
    """Handles all game logic and interfaces with UI via pygame."""

    title = 'Another Ordinary Weber Christmas'

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def start(self):
        """Let the sin... begin."""
        self.init()
        self.loop()

    def init(self):
        pg.init()

        # Sound.
        pg.mixer.init()

        # Window.
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.title)
        pg.mouse.set_visible(False)
        self.gamefont = pg.font.SysFont('Consolas', 16)
        self.clock = pg.time.Clock()

        # Compute player regions and start positions.
        weber_region = ((0, 0), (self.width, self.height / 2))             # top half.
        santa_region = ((0, self.height / 2), (self.width, self.height))   # bottom half.
        weber_pos = ((weber_region[1][0] + weber_region[0][0]) / 2, (weber_region[1][1] + weber_region[0][1]) / 2)
        santa_pos = ((santa_region[1][0] + santa_region[0][0]) / 2, (santa_region[1][1] + santa_region[0][1]) / 2)

        # TODO: Loading menu

        # Initialize players.
        self.groups = {
            'all': pg.sprite.RenderUpdates(),
        }
        Player.groups = self.groups['all']
        self.santa = Santa(santa_pos[0], santa_pos[1], santa_region, is_turn=True)
        self.weber = Benjamin(weber_pos[0], weber_pos[1], weber_region)
        self.current = self.santa

    def dialog(self, msg):
        """Draw dialog component in the middle of screen."""
        dialog_padding = 40
        dialog = self.gamefont.render(msg.upper(), 1, BLACK)
        dialog_rect = dialog.get_rect(center=(self.width / 2, self.height / 2))
        print(dialog_rect)
        # Draw.
        pg.draw.rect(self.screen, LIGHT_GRAY, (0, dialog_rect.top - dialog_padding, self.width, dialog_rect.bottom + dialog_padding))
        self.screen.blit(dialog, dialog_rect)
    
    def stats(self):
        """Display player stats."""

        health_fmt = 'HEALTH: {}'
        power_fmt = 'POWER: {}'
        xp_fmt = 'XP: {}'

        stat_color = GRAY 
        padding = 5 

        # Weber stats.
        weber_health = self.gamefont.render(health_fmt.format(self.weber.health), 1, stat_color)
        weber_health_rect = weber_health.get_rect(topright=(self.weber.bounded_region[1][0] - padding, self.weber.bounded_region[0][1] + padding))
        self.screen.blit(weber_health, weber_health_rect)

        weber_power = self.gamefont.render(power_fmt.format(self.weber.power), 1, stat_color)
        weber_power_rect = weber_power.get_rect(topright=(weber_health_rect.right, weber_health_rect.bottom + padding))
        self.screen.blit(weber_power, weber_power_rect)

        weber_xp = self.gamefont.render(xp_fmt.format(self.weber.xp), 1, stat_color)
        weber_xp_rect = weber_xp.get_rect(topright=(weber_power_rect.right, weber_power_rect.bottom + padding))
        self.screen.blit(weber_xp, weber_xp_rect)

        # Santa stats (on bottom).
        santa_health = self.gamefont.render(health_fmt.format(self.santa.health), 1, stat_color)
        santa_health_rect = santa_health.get_rect(bottomright=(self.santa.bounded_region[1][0] - padding, self.santa.bounded_region[1][1] - padding))
        self.screen.blit(santa_health, santa_health_rect)

        santa_power = self.gamefont.render(power_fmt.format(self.santa.power), 1, stat_color)
        santa_power_rect = santa_power.get_rect(bottomright=(santa_health_rect.right, santa_health_rect.top - padding))
        self.screen.blit(santa_power, santa_power_rect)

        santa_xp = self.gamefont.render(xp_fmt.format(self.santa.xp), 1, stat_color)
        santa_xp_rect = santa_xp.get_rect(bottomright=(santa_power_rect.right, santa_power_rect.top - padding))
        self.screen.blit(santa_xp, santa_xp_rect)


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

            # Wipe frame.
            self.screen.fill(WHITE)

            # Draw game environment and players.
            self.dialog('Santa: "Get ready for some hot suck of dick"')            
            self.stats()
            self.groups['all'].draw(self.screen)

            # Send results to screen.
            pg.display.flip()

            # Will make the loop run at the same speed all the time.
            self.clock.tick(FPS)

        pg.quit()
