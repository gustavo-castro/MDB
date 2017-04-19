import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

def terminate():
    pygame.quit()
    sys.exit()

class Character(pygame.sprite.Sprite):
    def __init__(self, Name, imagedict):
        pygame.sprite.Sprite.__init__(self)

        self.Name = Name
        self.imagedict = imagedict
        self.image = self.imagedict['down']
        self.rect = self.image.get_rect()
        randomstart = self.getRandomLocation()
        self.x = randomstart[0]
        self.y = randomstart[1]
        self.rect.x = self.x
        self.rect.y = self.y
        self.walls = None

    def getRandomLocation(self):
        return [random.randint(0, CELLWIDTH - 1),random.randint(0, CELLHEIGHT - 1)]

    def updatePosition(self, eventkey):
        aux = 0
        if (eventkey == K_LEFT or eventkey == K_a):
            self.x -= CELLSIZE
            self.rect.x = self.x
            self.image = self.imagedict['left']
            aux = 1
        elif (eventkey == K_RIGHT or eventkey == K_d):
            self.x += CELLSIZE
            self.rect.x = self.x
            self.image = self.imagedict['right']
            aux = 2
        elif (eventkey == K_UP or eventkey == K_w):
            self.y -= CELLSIZE
            self.rect.y = self.y
            self.image = self.imagedict['up']
            aux = 3
        elif (eventkey == K_DOWN or eventkey == K_s):
            self.y += CELLSIZE
            self.rect.y = self.y
            self.image = self.imagedict['down']
            aux = 4
        elif eventkey == K_ESCAPE:
            terminate()
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        if block_hit_list:
            if aux == 1:
                self.x += CELLSIZE
                self.rect.x = self.x
            elif aux == 2:
                self.x -= CELLSIZE
                self.rect.x = self.x
            elif aux == 3:
                self.y += CELLSIZE
                self.rect.x = self.x
            elif aux == 4:
                self.y -= CELLSIZE
                self.rect.x = self.x