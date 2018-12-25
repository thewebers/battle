import random

import pygame as pg
from pygame.locals import *

from .benjamin import Benjamin
from .component import *
from .entity import Entity
from .player import Player
from .santa import Santa
from .system import *

FPS = 30

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class DrawRect(pg.Rect):
    """PyGame `Rect` that can be drawn."""
    def draw(self, screen, color):
        pg.draw.rect(screen, color, self)


class Game:
    """Handles all game logic and interfaces with UI via pygame."""
    title = 'Another Ordinary Weber Christmas'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.systems = [
            PlayerUpdateSystem(),
            PositionBoundSystem(),
            PositionUpdateSystem(),
            VelocityAttenuateSystem(),
            AnimateUpdateSystem(),
            DrawUpdateSystem()
        ]
        self.entities = []

    def start(self):
        """Let the sin... begin."""
        self.init()
        self.run()

    def init(self):
        pg.init()

        # Sound
        pg.mixer.init()

        # Window
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.title)
        pg.mouse.set_visible(False)
        self.gamefont = pg.font.SysFont('Consolas', 16)
        self.clock = pg.time.Clock()

        # Compute player/dialog regions.
        DIALOG_HEIGHT = 100
        DIALOG_TOP = (self.height - DIALOG_HEIGHT) / 2
        DIALOG_BOTTOM = DIALOG_TOP + DIALOG_HEIGHT
        self.top_region = DrawRect(0, 0, self.width, DIALOG_TOP)
        self.middle_region = DrawRect(0, DIALOG_TOP, self.width, DIALOG_HEIGHT)
        self.bottom_region = DrawRect(0, DIALOG_BOTTOM, self.width, self.height - DIALOG_BOTTOM)

        # We only use a single PyGame group for all of our rendering, because
        # we have our own ECS architecture for organizing entities.
        self.sprite_group = pg.sprite.RenderUpdates()
        DrawComp.groups = self.sprite_group

        # Initialize a Weber.
        weber_x, weber_y = self.top_region.center
        self.weber = self.create_entity()
        Benjamin.init(self.weber, weber_x, weber_y, self.top_region)

        # Initialize Santa.
        santa_x, santa_y = self.bottom_region.center
        self.santa = self.create_entity()
        Santa.init(self.santa, santa_x, santa_y, self.bottom_region)

        self.current_player = self.santa
        self.santa.add_comp(TurnFlagComp())

    def run(self):
        running = True
        while running:
            # Poll the events.
            for event in pg.event.get():
                # Check if they tryna leave.
                close_requested = event.type == QUIT
                close_requested |= event.type == KEYDOWN and event.key == K_ESCAPE
                if close_requested:
                    running = False
            pressed_keys = pg.key.get_pressed()

            # Switch turns.
            if pressed_keys[K_s]:
                self.current_player.remove_comp(TurnFlagComp)
                if self.current_player == self.weber:
                    self.current_player = self.santa
                elif self.current_player == self.santa:
                    self.current_player = self.weber
                else:
                    assert False
                self.current_player.add_comp(TurnFlagComp())

            # Run systems.
            for system in self.systems:
                system.run(self.entities, pressed_keys)

            # Draw game environment and players.
            self.draw_dialog('Santa: "Get ready for some hot suck of dick"')
            self.draw_stats(self.weber, is_top_player=True)
            self.draw_stats(self.santa, is_top_player=False)
            self.sprite_group.draw(self.screen)

            # Send results to screen.
            pg.display.flip()

            # Will make the loop run at the same speed all the time.
            self.clock.tick(FPS)
        pg.quit()

    def create_entity(self):
        # TODO: Make generational index allocator.
        result_id = len(self.entities)
        result = Entity(result_id)
        self.entities.append(result)
        return result

    def destroy_entity(self, entity):
        assert(entity.ident < len(self.entities))
        assert(self.entities[entity.ident] is not None)
        self.entities[entity.ident] = None

    def draw_dialog(self, msg):
        """Draw dialog component in the middle of screen."""
        PADDING = 40
        # TODO: Maybe couple the rendering of regions with the regions that
        # confine the players.  Make a `Region` class?
        # TODO: Reconcile between the different coordinate systems being used
        # by rendering and the game world (i.e., y-axes being reversed).

        # Render dialog prompt (but don't blit it yet).
        dialog = self.gamefont.render(msg.upper(), 1, BLACK)
        dialog_rect = dialog.get_rect(center=(self.width / 2, self.height / 2))
        # Draw regions.
        self.top_region.draw(self.screen, WHITE)
        self.middle_region.draw(self.screen, LIGHT_GRAY)
        self.bottom_region.draw(self.screen, DARK_GRAY)
        # Blit dialog at the end, so it's not overwritten by blitting the region rects.
        self.screen.blit(dialog, dialog_rect)

    def draw_stats(self, player, is_top_player):
        PADDING = 5
        pos_bounds = player.get_comp(PositionBoundComp)
        if is_top_player:
            draw_color = DARK_GRAY
            pos_args = [
                lambda _: { 'bottomright': (pos_bounds.w - PADDING, pos_bounds.h - PADDING) },
                lambda rect: { 'bottomright': (rect.right, rect.top - PADDING) },
                lambda rect: { 'bottomright': (rect.right, rect.top - PADDING) },
            ]
        else:
            draw_color = WHITE
            pos_args = [
                lambda _: { 'topright': (pos_bounds.w - PADDING, pos_bounds.y + PADDING) },
                lambda rect: { 'topright': (rect.right, rect.bottom + PADDING) },
                lambda rect: { 'topright': (rect.right, rect.bottom + PADDING) },
            ]
        player_comp = player.get_comp(PlayerComp)
        health_rect = self.draw_text(f'HEALTH: {player_comp.curr_health} / {player_comp.max_health}', color=draw_color, **(pos_args[0](None)))
        power_rect = self.draw_text(f'POWER: {player_comp.curr_power} / {player_comp.max_power}', color=draw_color, **(pos_args[1](health_rect)))
        self.draw_text(f'DRUNKENNESS: {player_comp.curr_drunkenness} / {player_comp.max_drunkenness}', color=draw_color, **(pos_args[2](power_rect)))

    def draw_text(self, text, color=GRAY, **kwargs):
        """Draws `text` to the screen at the location described by `kwargs`.

        `kwargs` can contain any of the arguments for `Surface.get_rect` (e.g.,
        "topright").

        Returns the rectangle for the drawn text.
        """
        text_surface = self.gamefont.render(text, 1, color)
        text_rect = text_surface.get_rect(**kwargs)
        self.screen.blit(text_surface, text_rect)
        return text_rect
