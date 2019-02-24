from abc import ABC, abstractmethod
import math
import random


class Auto(ABC):
    @abstractmethod
    def act(self, input):
        """Act in environemnt based on current state/input."""
        raise NotImplementedError
    @abstractmethod
    def step(self, experience):
        """Update agent's internal model."""
        raise NotImplementedError


class ReinforceAuto(Auto):
    def __init__(self):
        self.learn_stepcount = 2000
        self.experiences = [] # TODO: Import ReplayBuffer
    def act(self, eingan):
        t = eingan['t']
        if t % self.learn_stepcount == 0:
            self._learn()
        return [random.random(), random.random()]
    def step(self, experience):
        pass
    def _learn(self):
        pass


class ManhattanAuto(Auto):
    UPDATE_RATE = 10
    SPEED = 3
    def __init__(self):
        self.memory = {}
    def act(self, eingan):
        # Check memory for past moves.
        counter = self.memory.get('counter', 0)
        update_vect = self.memory.get('update_vect', [0.0, 0.0])
        self.memory['counter'] = counter + 1
        # Stick in straight line before counter cycles.
        if counter % ManhattanAuto.UPDATE_RATE != 0:
            return
        # Move towards the opponent.
        pos = eingan['pos']
        # vel = eingan['vel']
        opp_pos = eingan['opp_pos']
        x_diff = opp_pos.x - pos.x
        y_diff = opp_pos.y - pos.y
        if abs(x_diff) > abs(y_diff):
            update_vect[0] = math.copysign(1, x_diff) * \
                             ManhattanAuto.SPEED * \
                             (1 + 1 ** -(abs(x_diff)))
            update_vect[1] = 0
        else:
            update_vect[0] = 0
            update_vect[1] = math.copysign(1, y_diff) * \
                             ManhattanAuto.SPEED * \
                             (1 + 1 ** -(abs(y_diff)))
        # vel.x = update_vect[0]
        # vel.y = update_vect[1]
        self.memory['update_vect'] = update_vect
        return update_vect
    def step(self, experience):
        pass

