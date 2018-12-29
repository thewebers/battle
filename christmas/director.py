from enum import Enum
import random

from .benjamin import Benjamin
from .component import *
from .dialog import EmptyFrame, BasicTextFrame, MugTextFrame
from .input_handler import InputIntent, CHOICE_INTENTS
from .projectile import CoalProjectile
from .santa import Santa


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
        self.remaining_time = BeginTurnState.STATE_DURATION
        player_name = self.player.get_comp(PlayerComp).name
        self.game.dialog_window.set_frame(BasicTextFrame(f'beginning of {player_name}\'s turn'))

    def update(self):
        self.remaining_time -= 1

    def is_finished(self):
        return self.remaining_time <= 0

    def get_next(self):
        return TurnQuoteState(self.game, self.player)


class TurnQuoteState(State):
    STATE_DURATION = 10

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.game.dialog_window.set_frame(
            MugTextFrame(self.game, self.player, random.choice(self.player.get_comp(PlayerComp).quotes)))
        self.remaining_time = TurnQuoteState.STATE_DURATION

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
        self.moves = player.get_comp(PlayerComp).moves
        inp_conf = self.player.get_comp(InputConfigComp)
        self.choice_keys = [inp_conf.key_map[intent] for intent in CHOICE_INTENTS]
        frame_text = ' '.join([f'({pg.key.name(key)}) {move.prompt}'
                               for key, move in zip(self.choice_keys, self.moves)])
        self.game.dialog_window.set_frame(MugTextFrame(self.game, self.player, frame_text))

    def update(self):
        inp_handler = self.game.get_input_handler()
        inp_conf = self.player.get_comp(InputConfigComp)
        keys_down = list(map(lambda k: inp_handler.is_key_down(k), self.choice_keys))
        if any(keys_down):
            self.chosen_move = self.moves[keys_down.index(True)]
            self.finished = True

    def is_finished(self):
        return self.finished

    def get_next(self):
        return BeginMoveState(self.game, self.player, self.chosen_move)


class BeginMoveState(State):
    STATE_DURATION = 10

    def __init__(self, game, player, move):
        self.game = game
        self.player = player
        self.move = move
        self.remaining_time = BeginMoveState.STATE_DURATION
        self.game.dialog_window.set_frame(MugTextFrame(self.game, self.player, self.move.description))
        for _ in range(3):
            self.player.force_get_comp(AmmoComp).rounds.append(CoalProjectile)

    def update(self):
        self.remaining_time -= 1

    def is_finished(self):
        return self.remaining_time <= 0

    def get_next(self):
        return EndTurnState(self.game, self.player)


class EndTurnState(State):
    STATE_DURATION = 10

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.remaining_time = EndTurnState.STATE_DURATION
        player_name = self.player.get_comp(PlayerComp).name
        self.game.dialog_window.set_frame(BasicTextFrame(f'end of {player_name}\'s turn'))

    def update(self):
        self.remaining_time -= 1

    def is_finished(self):
        return self.remaining_time <= 0

    def get_next(self):
        return BeginTurnState(self.game, self._get_other_player())

    def _get_other_player(self):
        if self.player == self.game.get_top_player():
            return self.game.get_bottom_player()
        elif self.player == self.game.get_bottom_player():
            return self.game.get_top_player()
        else:
            assert False

