
import pygame as pg
import random

from enum import Enum

from players.santa import Santa

WIDTH = 360
HEIGHT = 480
FPS = 30

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class UserActions(Enum):
    UP = 1
    LEFT = 2
    RIGHT = 3
    DOWN = 4

class GameEngine:
    '''Handles all game logic and interfaces with UI via pygame.'''
    def __init__(self, w=WIDTH, h=HEIGHT):
        self.santa = Santa(w//2, h//2)
        self.mortal = None
        self.player = self.santa

    def start(self):
        self.init()
        self.loop()

    def init(self):
        ## initialize pg and create window
        pg.init()
        pg.mixer.init()  ## For sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Another Ordinary Weber Christmas")
        self.clock = pg.time.Clock()     ## For syncing the FPS

        ## group all the sprites together for ease of update
        self.all_sprites = pg.sprite.Group()

        # We don't use no motherfucking mouse
        pg.mouse.set_visible(False)
    
    def process_event(self, event):
        # TODO: Take input from UI and process as a game action
        if event.type == 2: # key down 
            key = event.dict['key'] 
            if key == 273: # up
                self.player.move(0, -1)
            elif key == 276: # left
                self.player.move(-1, 0)
            elif key == 275: # right
                self.player.move(1, 0)
            elif key == 274: # down
                self.player.move(0, 1)

    def loop(self):
        ## Game loop
        running = True
        while running:

            #1 Process input/events
            self.clock.tick(FPS)     ## will make the loop run at the same speed all the time
            for event in pg.event.get():        # gets all the events which have occured till now and keeps tab of them.
                ## listening for the the X button at the top
                if event.type == pg.QUIT:
                    running = False
                self.process_event(event)        

            #2 Update
            self.all_sprites.update()

            #3 Draw/render
            self.screen.fill(WHITE)

            myfont = pg.font.SysFont("Comic Sans MS", 30)
            # apply it to text on a label
            label = myfont.render("beneth sucketh cocketh", 1, BLACK)
            # put the label object on the self.screen at point x=100, y=100
            self.screen.blit(label, (20, 100))

            self.all_sprites.draw(self.screen)

            for point in range(0,641,64): # range(start, stop, step)
                pg.draw.line(self.screen, (255,0,255), (0,0), (480, point), 1)

            ########################
            ### Your code comes here
            ########################
            # TODO: Draw all the sprites, mothafucka 

            ## Done after drawing everything to the self.screen
            pg.display.flip()       

        pg.quit()
