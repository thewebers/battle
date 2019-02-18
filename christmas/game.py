import random

from pygame.locals import *
import pygame as pg

from .ben import Benjamin
from .color import *
from .component import *
from .dee import DeAnne
from .dialog import DialogWindow
from .director import Director
from .entity import Entity
from .globe import SnowGlobe
from .input_handler import InputHandler
from .janic import Janicolous
from .josh import Joshua
from .logan import Logan
from .luke import Lucas
from .player import Player
from .projectile import Projectile
from .rob import Robert
from .santa import Santa
from .sound import Sound, SoundType
from .system import *
from .util import DrawRect

FPS = 30


class Game:
    """Handles all game logic and interfaces with UI via pygame."""
    TITLE = 'Another Ordinary Weber Christmas'
    FG_COLOR = GRAY
    BG_COLOR = WHITE

    def __init__(self, width, height, debug_mode=False):
        self._debug_mode = debug_mode
        self.width = width
        self.height = height
        self.systems = [
            PlayerUpdateSystem(self),
            AutonomousUpdateSystem(self),
            AmmoUpdateSystem(self),
            PositionBoundBounceSystem(self),
            CollideSystem(self),
            PositionUpdateSystem(self),
            VelocityAttenuateSystem(self),
            LifetimeUpdateSystem(self),
            OutOfBoundsCleanupSystem(self),
            DeadCleanupSystem(self),
            PlayerAnimateUpdateSystem(self),
            AnimateUpdateSystem(self),
            DrawUpdateSystem(self),
            SnowParticleUpdateSystem(self),
            ScheduleSystem(self),
        ]
        self.webers = [
            Benjamin,
            DeAnne,
            Janicolous,
            Joshua,
            Logan,
            Lucas,
            Robert
        ]
        self.entities = []
        self.input_handler = InputHandler()

    def start(self):
        """Let the sin... begin."""
        self.init()
        self.run()

    def init(self):
        pg.init()

        # Game Music and Sound
        self.sound = Sound(debug_mode=self._debug_mode)

        # Window
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(Game.TITLE)
        pg.mouse.set_visible(False)
        self.font = pg.font.Font('res/font/8-bitpusab.ttf', 10)
        self.clock = pg.time.Clock()

        # Compute player/dialog regions.
        # NB: The dialog window is between the top region and the bottom region.
        self.dialog_window = DialogWindow(self.width, self.height, self.font,
                                          self.FG_COLOR, GREEN)
        dialog_rect = self.dialog_window.get_rect()
        self.top_region = DrawRect(0, 0, self.width, dialog_rect.top, \
                                   Game.BG_COLOR)
        self.bottom_region = DrawRect(0,
                                      dialog_rect.bottom,
                                      self.width,
                                      self.height - dialog_rect.bottom,
                                      Game.BG_COLOR)

        # We only use a single PyGame group for all of our rendering, because
        # we have our own ECS architecture for organizing entities.
        self.sprite_group = pg.sprite.RenderUpdates()
        DrawComp.groups = self.sprite_group

        # Static Initialization
        Projectile.static_init(self.width, self.height)

        # Initialize a Weber.
        weber_x, weber_y = self.top_region.center
        self.top_player = self.create_entity()
        random.choice(self.webers).init(self.top_player, weber_x, weber_y, \
                                        self.top_region)
        weber_pos = self.top_player.get_comp(PositionComp)
        weber_pos.x -= self.top_player.get_comp(SizeComp).w / 2
        weber_pos.y -= self.top_player.get_comp(SizeComp).h / 2

        # Initialize Santa.
        santa_x, santa_y = self.bottom_region.center
        self.bottom_player = self.create_entity()
        Santa.init(self.bottom_player, santa_x, santa_y, self.bottom_region)
        santa_pos = self.bottom_player.get_comp(PositionComp)
        santa_pos.x -= self.bottom_player.get_comp(SizeComp).w / 2
        santa_pos.y -= self.bottom_player.get_comp(SizeComp).h / 2

        # The director needs to be initted *after* the players have been
        # initted.
        self.director = Director(self)

        # Create ornament spawning job, as system.
        ornament_job_entity = self.create_entity()
        ornament_job_entity.add_comp(JobScheduleComp('spawn_orn', 30000, 2000))
        beer_job_entity = self.create_entity()
        beer_job_entity.add_comp(JobScheduleComp('spawn_beer', 60000,
                                                     10000))

        # Initialize snowglobe.
        self.globe = SnowGlobe(self.width, self.height, self.create_entity, \
                               debug_mode=self._debug_mode)

    def run(self):
        while True:
            self.input_handler.update()
            if self.input_handler.is_close_requested():
                # End game loop.
                break

            self.director.update()
            self.dialog_window.update()
            # Run systems.
            for system in self.systems:
                system.run()

            # Draw game environment.
            self.top_region.draw(self.screen)
            self.dialog_window.draw(self.screen)
            self.bottom_region.draw(self.screen)
            self.draw_stats(self.top_player)
            self.draw_stats(self.bottom_player)
            self.globe.shake()

            # Draw entities.
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
        # TODO: `Game` shouldn't have to worry about killing `DrawComp`s.
        if entity.has_comp(DrawComp):
            entity.get_comp(DrawComp).kill()
        self.entities[entity.ident] = None

    def draw_stats(self, player):
        PADDING = 5
        pos_bounds = player.get_comp(PositionBoundComp)
        draw_color = Game.FG_COLOR
        if player.has_comp(TopPlayerFlag):
            pos_args = [
                lambda _: { 'bottomright': (pos_bounds.w - PADDING, \
                                            pos_bounds.h - PADDING) },
                lambda rect: { 'bottomright': (rect.right, rect.top - PADDING) },
                lambda rect: { 'bottomright': (rect.right, rect.top - PADDING) },
            ]
        elif player.has_comp(BottomPlayerFlag):
            pos_args = [
                lambda _: { 'topright': (pos_bounds.w - PADDING, pos_bounds.y + PADDING) },
                lambda rect: { 'topright': (rect.right, rect.bottom + PADDING) },
                lambda rect: { 'topright': (rect.right, rect.bottom + PADDING) },
            ]
        else:
            assert False
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

    def get_top_player(self):
        return self.top_player

    def get_bottom_player(self):
        return self.bottom_player

    def get_input_handler(self):
        return self.input_handler
