from enum import Enum
import random

from .benjamin import Benjamin
from .component import *
from .dialog import EmptyFrame, BasicTextFrame, MugTextFrame
from .santa import CoalProjectile, Santa


class Director:
    def __init__(self, game):
        self.state = BeginState(game)
        self.game = game

    def update(self):
        self.state.update()
        if self.state.is_finished():
            self.state = self.state.get_next()


class State:
    def __init__(self, game):
        self.game = game

    def update(self):
        assert False

    def is_finished(self):
        assert False

    def get_next(self):
        assert False


class BeginState(State):
    STATE_DURATION = 10

    def __init__(self, game):
        self.game = game
        self.remaining_time = BeginState.STATE_DURATION
        # Choose starting player.
        self.player = random.choice([game.get_top_player(), game.get_bottom_player()])

    def update(self):
        self.remaining_time -= 1

    def is_finished(self):
        return self.remaining_time <= 0

    def get_next(self):
        return BeginTurnState(self.game, self.player)


class BeginTurnState(State):
    STATE_DURATION = 10

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.game.dialog_window.set_frame(
            MugTextFrame(self.game, self.player, random.choice(self.player.get_comp(QuoteComp).quotes)))
        self.remaining_time = BeginTurnState.STATE_DURATION

    def update(self):
        self.remaining_time -= 1

    def is_finished(self):
        return self.remaining_time <= 0

    def get_next(self):
        return MoveSelectState(self.game, self.player)


class MoveSelectState(State):
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.finished = False
        self.game.dialog_window.set_frame(
            BasicTextFrame(' | '.join(map(lambda m: m.prompt,
                                          player.get_comp(MoveSelectComp).moves))))

    def update(self):
        inp_handler = self.game.get_input_handler()
        for move in self.player.get_comp(MoveSelectComp).moves:
            if inp_handler.is_key_pressed(move.key):
                self.chosen_move = move
                self.finished = True
                break

    def is_finished(self):
        return self.finished

    def get_next(self):
        return MoveBeginState(self.game, self.player, self.chosen_move)


class MoveBeginState(State):
    STATE_DURATION = 10

    def __init__(self, game, player, move):
        self.game = game
        self.player = player
        self.move = move
        self.remaining_time = MoveBeginState.STATE_DURATION
        self.game.dialog_window.set_frame(MugTextFrame(self.game, self.player, self.move.description))
        for _ in range(3):
            self.player.force_get_comp(AmmoComp).rounds.append(CoalProjectile)

    def update(self):
        self.remaining_time -= 1

    def is_finished(self):
        return self.remaining_time <= 0

    def get_next(self):
        return BetweenTurnState(self.game, self.player)


class BetweenTurnState(State):
    STATE_DURATION = 10

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.remaining_time = BetweenTurnState.STATE_DURATION
        self.game.dialog_window.set_frame(EmptyFrame())

    def update(self):
        self.remaining_time -= 1

    def is_finished(self):
        return self.remaining_time <= 0

    def get_next(self):
        if self.player == self.game.get_top_player():
            return BeginTurnState(self.game, self.game.get_bottom_player())
        elif self.player == self.game.get_bottom_player():
            return BeginTurnState(self.game, self.game.get_top_player())
        else:
            assert False
