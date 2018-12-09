class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = None
    def attach(self, sprite):
        self.sprite = sprite
    