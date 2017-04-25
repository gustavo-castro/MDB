import pygame
from pygame.locals import *

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

class TitleScreen(object):
    "Class that defines the main title screen"
    
    def __init__(self, DISPLAYSURF, basicfont, fpsclock, fps, window_width, window_height):
        self.font = 'freesansbold.ttf'
        self.name = 'Mecanismos de Batalha'
        self.screen = DISPLAYSURF
        self.basicfont = basicfont
        self.fpsclock = fpsclock
        self.fps = fps
        self.window_width = window_width
        self.window_height = window_height

    def drawPressKeyMsg(self):
        pressKeySurf = self.basicfont.render('Press a key to play.', True, DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (self.window_width - 200, self.window_height - 30)
        self.screen.blit(pressKeySurf, pressKeyRect)

    def drawStartScreen(self):
        titleFont = pygame.font.Font(self.font, 30)
        titleSurf1 = titleFont.render(self.name, True, RED, BLACK)
        titleRect1 = titleSurf1.get_rect()
        self.screen.fill(BGCOLOR)
        titleRect1.center = (self.window_width / 2, self.window_height / 2)
        self.screen.blit(titleSurf1, titleRect1)
        self.drawPressKeyMsg()

    def drawGameOverScreen(self):
        gameOverFont = pygame.font.Font(self.font, 150)
        gameSurf = gameOverFont.render('Game', True, WHITE)
        overSurf = gameOverFont.render('Over', True, WHITE)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (self.window_width / 2, 10)
        overRect.midtop = (self.window_width / 2, gameRect.height + 10 + 25)
        self.screen.blit(gameSurf, gameRect)
        self.screen.blit(overSurf, overRect)
        self.drawPressKeyMsg()

    def drawWinnerScreen(self):
        youWonFont = pygame.font.Font(self.font, 150)
        youSurf = youWonFont.render('You', True, WHITE)
        wonSurf = youWonFont.render('Won', True, WHITE)
        youRect = youSurf.get_rect()
        wonRect = wonSurf.get_rect()
        youRect.midtop = (self.window_width / 2, 10)
        wonRect.midtop = (self.window_width / 2, youRect.height + 10 + 25)
        self.screen.blit(youSurf, youRect)
        self.screen.blit(wonSurf, wonRect)
        self.drawPressKeyMsg()