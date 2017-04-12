#Mecanismos de Batalha

import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Mecanismos de Batalha')
    MarcusImage = pygame.image.load('boy.png')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():
    # Set a random start point.
    MarcusCoords = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a):
                    MarcusCoords = {'x': MarcusCoords['x'] - 1, 'y': MarcusCoords['y']}
                elif (event.key == K_RIGHT or event.key == K_d):
                    MarcusCoords = {'x': MarcusCoords['x'] + 1, 'y': MarcusCoords['y']}
                elif (event.key == K_UP or event.key == K_w):
                    MarcusCoords = {'x': MarcusCoords['x'], 'y': MarcusCoords['y'] - 1}
                elif (event.key == K_DOWN or event.key == K_s):
                    MarcusCoords = {'x': MarcusCoords['x'], 'y': MarcusCoords['y'] + 1}
                elif event.key == K_ESCAPE:
                    terminate()

        DISPLAYSURF.fill(BGCOLOR)
        drawApple(MarcusCoords)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 30)
    titleSurf1 = titleFont.render('Mecanismos de Batalha', True, RED, BLACK)
    titleRect1 = titleSurf1.get_rect()

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        titleRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(titleSurf1, titleRect1)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

if __name__ == '__main__':
    main()