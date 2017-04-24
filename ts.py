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

class TitleScreen(object):
    "Class that defines the main title screen"
    
    def __init__(self, DISPLAYSURF, BASICFONT, FPSCLOCK):
        self.font = 'freesansbold.ttf'
        self.name = 'Mecanismos de Batalha'
        self.screen = DISPLAYSURF
        self.basicfont = BASICFONT
        self.fps = FPSCLOCK

    def checkForKeyPress(self):
        if len(pygame.event.get(QUIT)) > 0:
            terminate()

        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            terminate()
        return keyUpEvents[0].key

    def drawPressKeyMsg(self):
        pressKeySurf = self.basicfont.render('Press a key to play.', True, DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
        self.screen.blit(pressKeySurf, pressKeyRect)

    def showStartScreen(self):
        RED       = (255,   0,   0)
        titleFont = pygame.font.Font(self.font, 30)
        titleSurf1 = titleFont.render(self.name, True, RED, BLACK)
        titleRect1 = titleSurf1.get_rect()

        while True:
            self.screen.fill(BGCOLOR)
            titleRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
            self.screen.blit(titleSurf1, titleRect1)

            self.drawPressKeyMsg()

            if self.checkForKeyPress():
                pygame.event.get() # clear event queue
                return
            pygame.display.update()
            self.fps.tick(FPS)

    def showGameOverScreen(self):
        WHITE     = (255, 255, 255)
        gameOverFont = pygame.font.Font(self.font, 150)
        gameSurf = gameOverFont.render('Game', True, WHITE)
        overSurf = gameOverFont.render('Over', True, WHITE)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (WINDOWWIDTH / 2, 10)
        overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

        self.screen.blit(gameSurf, gameRect)
        self.screen.blit(overSurf, overRect)
        self.drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)
        self.checkForKeyPress() # clear out any key presses in the event queue

        while True:
            if self.checkForKeyPress():
                pygame.event.get() # clear event queue
                return