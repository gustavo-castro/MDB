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

class Character(pygame.sprite.Sprite):
    def __init__(self, Name, image):
        self.Name = Name
        self.image = image
        #self.image = pygame.transform.scale(self.image, (CELLSIZE+5, CELLSIZE+5))
        randomstart = self.getRandomLocation()
        self.x = randomstart[0]
        self.y = randomstart[1]

    def getRandomLocation(self):
        return [random.randint(0, CELLWIDTH - 1),random.randint(0, CELLHEIGHT - 1)]

    def drawCharacter(self, DISPLAYSURF):
        x = self.x * CELLSIZE
        y = self.y * CELLSIZE
        Rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        #pygame.draw.rect(DISPLAYSURF, RED, Rect)
        #descobrir como ajeitar esse treco feio aqui
        DISPLAYSURF.blit(self.image, self.image.get_rect(center=(x+8, y+5)))

    def updateposition(self, eventkey):
        if (eventkey == K_LEFT or eventkey == K_a):
            self.x -= 1
        elif (eventkey == K_RIGHT or eventkey == K_d):
            self.x += 1
        elif (eventkey == K_UP or eventkey == K_w):
            self.y -= 1
        elif (eventkey == K_DOWN or eventkey == K_s):
            self.y += 1
        elif eventkey == K_ESCAPE:
            terminate()