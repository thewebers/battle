from collections import deque

from .color import *
from .component import *
from .util import DrawRect


class EmptyFrame:
    def update(self, *_):
        pass

    def draw(self, *_):
        pass


class DialogWindow:
    HEIGHT = 100
    EMPTY_FRAME = EmptyFrame()

    def __init__(self, screen_width, screen_height, font):
        self.queue = deque()
        window_top = (screen_height - DialogWindow.HEIGHT) / 2
        window_bottom = window_top + DialogWindow.HEIGHT
        self.screen_region = DrawRect(0, window_top, screen_width, DialogWindow.HEIGHT)
        self.font = font

    def update(self):
        self.curr_frame = self.get_curr_frame()
        self.curr_frame.update(self.screen_region)

    def draw(self, screen):
        self.screen_region.draw(screen, DARK_GRAY)
        self.curr_frame.draw(self.font, self.screen_region, screen)

    def enqueue(self, frame):
        self.queue.append(frame)

    def get_curr_frame(self):
        if len(self.queue) == 0:
            return DialogWindow.EMPTY_FRAME

        if isinstance(self.queue[0], tuple):
            # The current frame hasn't been initialized yet.  So we initialize
            # it, then place the result at the front of the queue.
            frame_constructor, frame_args = self.queue[0]
            self.queue[0] = frame_constructor(*frame_args)

        if self.queue[0].is_finished():
            # The current frame is finished.  Destroy it and recurse to find
            # the new one.
            self.queue.popleft().destroy()
            return self.get_curr_frame()
        else:
            return self.queue[0]

    def get_rect(self):
        return self.screen_region


class QuoteFrame:
    DURATION = 30
    MUG_X_PAD = 10

    def __init__(self, game, sprites, text):
        self.game = game
        self.mug = self.game.create_entity()
        self.mug.add_comp(DrawComp(sprites))
        self.mug.add_comp(PositionComp(0, 0))
        self.text = text
        self.remaining_time = QuoteFrame.DURATION

    def update(self, region):
        self.remaining_time -= 1
        pos = self.mug.get_comp(PositionComp)
        draw = self.mug.get_comp(DrawComp)
        pos.x = QuoteFrame.MUG_X_PAD
        pos.y = region.centery - draw.rect.h / 2

    def draw(self, font, region, screen):
        dialog = font.render(self.text.upper(), 1, WHITE)
        mugshot_x_offs = self.mug.get_comp(PositionComp).x
        mugshot_x_offs += self.mug.get_comp(DrawComp).rect.w + QuoteFrame.MUG_X_PAD
        mugshot_x_offs += QuoteFrame.MUG_X_PAD
        dialog_rect = dialog.get_rect(midleft=(mugshot_x_offs, region.centery))
        screen.blit(dialog, dialog_rect)

    def destroy(self):
        self.mug.kill()

    def is_finished(self):
        return self.remaining_time <= 0
