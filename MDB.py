#Mecanismos de Batalha

import random, pygame, sys
from pygame.locals import *
import characters
import ts

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

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, FONT, NAME, MarcusImage
    NAME = 'Mecanismos de Batalha'
    FONT = 'freesansbold.ttf'

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font(FONT, 18)
    pygame.display.set_caption(NAME)
    MarcusImage = pygame.image.load('boy.png')

    newtitlescreen = ts.TitleScreen()
    newtitlescreen.showStartScreen(DISPLAYSURF, BASICFONT, FPSCLOCK)
    while True:
        runGame()
        newtitlescreen.showGameOverScreen()

def runGame():
    # Initiate main character
    Marcus = characters.Character('Marcus', MarcusImage)

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                Marcus.updateposition(event.key)

        DISPLAYSURF.fill(BGCOLOR)
        Marcus.drawCharacter(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()