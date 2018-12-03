
from .player import Player

class Santa(Player):
    '''Drunk AI santa.'''
    # TODO: Implement from Player interface
    def __init__(self, x, y):
        Player.__init__(self, x, y)
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        print('Santa is on the motherfucking move', self.x, self.y)