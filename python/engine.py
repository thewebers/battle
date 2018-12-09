
import pygame as pg
import random

from enum import Enum

from players.santa import Santa
from sprites.santasprite import SantaSprite

WIDTH = 20
HEIGHT = 35
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
    def __init__(self, block_width=WIDTH, block_height=HEIGHT, pixel_to_block_ratio=25):

        assert block_height > block_width >= 10

        # Dimensions
        self.pixel_to_block_ratio = pixel_to_block_ratio
        self.bwidth = block_width
        self.bheight = block_height
        self.pwidth = block_width * self.pixel_to_block_ratio 
        self.pheight= block_height * self.pixel_to_block_ratio 

        # Players
        self.santa = Santa(self.bwidth//2, self.bheight//2)
        self.mortal = None
        self.player = self.santa

        self.timer = 0

    def start(self):
        '''Let the sin... begin.'''
        self.init()
        self.loop()

    def init(self):
        ## initialize pg and create window
        pg.init()
        pg.mixer.init()  ## For sound
        self.screen = pg.display.set_mode((self.pwidth, self.pheight))
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

            print(self.timer)

            #2 Update
            self.all_sprites.update()

            #3 Draw/render
            # self.screen.fill(WHITE)

            # myfont = pg.font.SysFont("Comic Sans MS", 30)
            # # apply it to text on a label
            # label = myfont.render("teeny weeny in ben's tummy", 1, BLACK)
            # # put the label object on the self.screen at point x=100, y=100
            # self.screen.blit(label, (20, 100))

            self.all_sprites.draw(self.screen)

            ########################
            ### Your code comes here
            ########################
            # TODO: Draw all the sprites, mothafucka 

            x, y = (self.player.x * self.pixel_to_block_ratio, self.player.y * self.pixel_to_block_ratio)
            santa_sprite = SantaSprite()
            self.santa.attach(santa_sprite)
            surface = santa_sprite.get_surface()
            
            # self.screen.blit(surface, (x, y))

            #pg.draw.line(self.screen, (255,0,255), (0,0), (self.player.x * self.pixel_to_block_ratio, self.player.y * self.pixel_to_block_ratio), 1)
            pg.draw.ellipse(self.screen, RED, (x, y, self.pixel_to_block_ratio, self.pixel_to_block_ratio))

            ## Done after drawing everything to the self.screen
            pg.display.flip()       

            self.timer += 1

        pg.quit()