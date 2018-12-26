import random

import pygame as pg
from pygame.locals import *

from .benjamin import Benjamin, BenjaminMug
from .color import *
from .component import *
from .dialog import DialogWindow, QuoteFrame
from .entity import Entity
from .player import Player
from .santa import Santa, SantaMug
from .system import *
from .util import DrawRect

FPS = 30


class Game:
    """Handles all game logic and interfaces with UI via pygame."""
    title = 'Another Ordinary Weber Christmas'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.systems = [
            WeberUpdateSystem(self),
            SantaUpdateSystem(self),
            PositionBoundSystem(self),
            PositionUpdateSystem(self),
            VelocityAttenuateSystem(self),
            LifetimeUpdateSystem(self),
            DeadCleanupSystem(self),
            PlayerAnimateUpdateSystem(self),
            AnimateUpdateSystem(self),
            DrawUpdateSystem(self)
        ]
        self.entities = []
        self.pressed_keys = {}

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
        self.font = pg.font.SysFont('Consolas', 14)
        self.clock = pg.time.Clock()

        # Compute player/dialog regions.
        # NB: The dialog window is between the top region and the bottom region.
        self.dialog_window = DialogWindow(self.width, self.height, self.font)
        dialog_rect = self.dialog_window.get_rect()
        self.top_region = DrawRect(0, 0, self.width, dialog_rect.top)
        self.bottom_region = DrawRect(0, dialog_rect.bottom,
                                      self.width, self.height - dialog_rect.bottom)

        # We only use a single PyGame group for all of our rendering, because
        # we have our own ECS architecture for organizing entities.
        self.sprite_group = pg.sprite.RenderUpdates()
        DrawComp.groups = self.sprite_group

        # Initialize a Weber.
        weber_x, weber_y = self.top_region.center
        self.weber = self.create_entity()
        Benjamin.init(self.weber, weber_x, weber_y, self.top_region)
        self.weber.get_comp(PositionComp).x -= self.weber.get_comp(SizeComp).w / 2
        self.weber.get_comp(PositionComp).y -= self.weber.get_comp(SizeComp).h / 2

        # Initialize Santa.
        santa_x, santa_y = self.bottom_region.center
        self.santa = self.create_entity()
        Santa.init(self.santa, santa_x, santa_y, self.bottom_region)
        self.santa.get_comp(PositionComp).x -= self.santa.get_comp(SizeComp).w / 2
        self.santa.get_comp(PositionComp).y -= self.santa.get_comp(SizeComp).h / 2

        self.current_player = self.santa
        self.santa.add_comp(TurnFlagComp())

    def run(self):
        running = True
        while running:
            # Poll the events.
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    self.pressed_keys[event.key] = True
                elif event.type == KEYUP:
                    self.pressed_keys[event.key] = False
                # Check if they tryna leave.
                close_requested = event.type == QUIT
                close_requested |= self.is_key_pressed(K_ESCAPE)
                if close_requested:
                    running = False

            if self.is_key_pressed(K_TAB):
                self.switch_turns()

            self.dialog_window.update()
            # Run systems.
            for system in self.systems:
                system.run()

            # Draw game environment.
            self.top_region.draw(self.screen, RED)
            self.dialog_window.draw(self.screen)
            self.bottom_region.draw(self.screen, GREEN)
            self.draw_stats(self.weber, is_top_player=True)
            self.draw_stats(self.santa, is_top_player=False)

            # Draw entities.
            self.sprite_group.draw(self.screen)

            # Send results to screen.
            pg.display.flip()

            # Will make the loop run at the same speed all the time.
            self.clock.tick(FPS)
        pg.quit()

    def switch_turns(self):
        self.current_player.remove_comp(TurnFlagComp)
        if self.current_player == self.weber:
            self.current_player = self.santa
            sprites = SantaMug.SPRITES
            quote = random.choice(Santa.QUOTES)
        elif self.current_player == self.santa:
            self.current_player = self.weber
            sprites = BenjaminMug.SPRITES
            quote = random.choice(Benjamin.QUOTES)
        else:
            assert False
        self.dialog_window.enqueue((QuoteFrame, [self, sprites, quote]))
        self.current_player.add_comp(TurnFlagComp())

    def create_entity(self):
        # TODO: Make generational index allocator.
        result_id = len(self.entities)
        result = Entity(result_id)
        self.entities.append(result)
        return result

    def destroy_entity(self, entity):
        assert(entity.ident < len(self.entities))
        assert(self.entities[entity.ident] is not None)
        # TODO: `Game` shouldn't have to worry about killing `DrawComp`s.
        if entity.has_comp(DrawComp):
            entity.get_comp(DrawComp).kill()
        self.entities[entity.ident] = None

    def draw_stats(self, player, is_top_player):
        PADDING = 5
        pos_bounds = player.get_comp(PositionBoundComp)
        draw_color = DARK_GRAY
        if is_top_player:
            pos_args = [
                lambda _: { 'bottomright': (pos_bounds.w - PADDING, pos_bounds.h - PADDING) },
                lambda rect: { 'bottomright': (rect.right, rect.top - PADDING) },
                lambda rect: { 'bottomright': (rect.right, rect.top - PADDING) },
            ]
        else:
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
        text_surface = self.font.render(text, 1, color)
        text_rect = text_surface.get_rect(**kwargs)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def is_key_pressed(self, key):
        return self.pressed_keys.get(key, False)
