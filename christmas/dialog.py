from collections import deque

from .color import *
from .component import *
from .util import DrawRect

FG_COLOR = BLACK
BG_COLOR = WHITE


class DialogWindow:
    HEIGHT = 100

    def __init__(self, screen_width, screen_height, font, fg_color, bg_color):
        window_top = (screen_height - DialogWindow.HEIGHT) / 2
        window_bottom = window_top + DialogWindow.HEIGHT
        self.screen_region = DrawRect(0, window_top, screen_width, DialogWindow.HEIGHT, bg_color)
        self.font = font
        self.frame = EmptyFrame()

    def update(self):
        self.frame.update(self.screen_region)

    def draw(self, screen):
        self.screen_region.draw(screen)
        self.frame.draw(self.font, self.screen_region, screen)

    def set_frame(self, frame):
        self.frame.destroy()
        self.frame = frame

    def get_rect(self):
        return self.screen_region


class DialogFrame:
    def __init__(self):
        assert False

    def update(self, region):
        assert False

    def draw(self, font, region, screen):
        assert False

    def destroy(self):
        assert False

    def is_finished(self):
        assert False


class EmptyFrame:
    def update(self, *_):
        pass

    def draw(self, *_):
        pass

    def destroy(self):
        pass


class BasicTextFrame(DialogFrame):
    def __init__(self, text):
        self.text = text

    def update(self, region):
        pass

    def draw(self, font, region, screen):
        dialog = font.render(self.text.upper(), 1, FG_COLOR)
        dialog_rect = dialog.get_rect(center=region.center)
        screen.blit(dialog, dialog_rect)

    def destroy(self):
        pass


class MugTextFrame(DialogFrame):
    MUG_LEFT_X_PAD = 8
    MUG_RIGHT_X_PAD = 3
    DEFAULT_ANIM_DELAY = 10

    def __init__(self, game, player, text):
        self.game = game
        self.mug = self.game.create_entity()
        self.mug.add_comp(DrawComp(player.get_comp(PlayerComp).mug_sprites))
        self.mug.add_comp(PositionComp(0, 0))
        self.mug.add_comp(AnimateComp(MugTextFrame.DEFAULT_ANIM_DELAY))
        self.text = text

    def update(self, region):
        pos = self.mug.get_comp(PositionComp)
        draw = self.mug.get_comp(DrawComp)
        pos.x = MugTextFrame.MUG_LEFT_X_PAD
        pos.y = region.centery - draw.rect.h / 2

    def draw(self, font, region, screen):
        dialog = font.render(self.text.upper(), 1, FG_COLOR)
        mugshot_x_offs = self.mug.get_comp(PositionComp).x
        mugshot_x_offs += MugTextFrame.MUG_LEFT_X_PAD + self.mug.get_comp(DrawComp).rect.w
        mugshot_x_offs += MugTextFrame.MUG_RIGHT_X_PAD
        dialog_rect = dialog.get_rect(midleft=(mugshot_x_offs, region.centery))
        screen.blit(dialog, dialog_rect)

    def destroy(self):
        self.mug.kill()
