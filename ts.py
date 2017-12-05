import pygame

import color


class TitleScreen(object):
    """Class that defines the main title screen"""
    def __init__(self, basicfont, fpsclock, screen):
        self.font = 'freesansbold.ttf'
        self.name = 'Mecanismos de Batalha'
        self.display = screen.display
        self.basicfont = basicfont
        self.fpsclock = fpsclock
        self.fps = screen.fps
        self.window_width = screen.width
        self.window_height = screen.height

    def drawPressKeyMsg(self):
        pressKeySurf = self.basicfont.render(
            'Press a key to play.', True, color.DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (
            self.window_width - 200, self.window_height - 30)
        self.display.blit(pressKeySurf, pressKeyRect)

    def drawStartScreen(self, which):
        background = pygame.image.load('Images/mainimage.png')
        self.display.blit(background, [0, 0])
        titleFont = pygame.font.Font(self.font, 30)
        titleSurf1 = titleFont.render(self.name, True, color.DARKGRAY)
        titleRect1 = titleSurf1.get_rect()
        titleRect1.center = (self.window_width / 2, 100)
        self.display.blit(titleSurf1, titleRect1)
        self.drawPressChooseModeScreen(which)

    def drawPressChooseModeScreen(self, which):
        whichstring = {0: 'Single Player', 1: 'Battle (two players)',
                       2: 'Coop (two players)'}
        aux = whichstring[which]
        allgamemodes = {'Single Player': 20, 'Battle (two players)': 40,
                        'Coop (two players)': 60}
        for gamemode in allgamemodes:
            if aux == gamemode:
                pressKeySurf = self.basicfont.render(gamemode, True, color.RED)
            else:
                pressKeySurf = self.basicfont.render(
                    gamemode, True, color.YELLOW)
            pressKeyRect = pressKeySurf.get_rect()
            pressKeyRect.center = (self.window_width/2, self.window_height/2 +
                                   allgamemodes[gamemode])
            self.display.blit(pressKeySurf, pressKeyRect)

    def drawGameOverScreen(self):
        gameOverFont = pygame.font.Font(self.font, 150)
        gameSurf = gameOverFont.render('Game', True, color.RED)
        overSurf = gameOverFont.render('Over', True, color.RED)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (self.window_width / 2, 10)
        overRect.midtop = (self.window_width / 2, gameRect.height + 10 + 25)
        self.display.blit(gameSurf, gameRect)
        self.display.blit(overSurf, overRect)
        self.drawPressKeyMsg()

    def drawWinnerScreen(self):
        youWonFont = pygame.font.Font(self.font, 150)
        youSurf = youWonFont.render('You', True, color.BLUE)
        wonSurf = youWonFont.render('Won', True, color.BLUE)
        youRect = youSurf.get_rect()
        wonRect = wonSurf.get_rect()
        youRect.midtop = (self.window_width / 2, 10)
        wonRect.midtop = (self.window_width / 2, youRect.height + 10 + 25)
        self.display.blit(youSurf, youRect)
        self.display.blit(wonSurf, wonRect)
        self.drawPressKeyMsg()

    def drawBatlleWinnerScreen(self, Player):
        youWonFont = pygame.font.Font(self.font, 150)
        youSurf = youWonFont.render('Player '+str(Player), True, color.BLUE)
        wonSurf = youWonFont.render('Won', True, color.BLUE)
        youRect = youSurf.get_rect()
        wonRect = wonSurf.get_rect()
        youRect.midtop = (self.window_width / 2, 10)
        wonRect.midtop = (self.window_width / 2, youRect.height + 10 + 25)
        self.display.blit(youSurf, youRect)
        self.display.blit(wonSurf, wonRect)
        self.drawPressKeyMsg()

    def drawPauseScreen(self, which):
        whichstring = {0: 'Unpause', 1: 'Change Mode', 2: 'Quit'}
        aux = whichstring[which]
        allgamemodes = {'Unpause': 20, 'Change Mode': 40, 'Quit': 60}
        for gamemode in allgamemodes:
            if aux == gamemode:
                pressKeySurf = self.basicfont.render(
                    gamemode, True, color.BLUE)
            else:
                pressKeySurf = self.basicfont.render(
                    gamemode, True, color.BLACK)
            pressKeyRect = pressKeySurf.get_rect()
            pressKeyRect.center = (self.window_width/2, self.window_height/2 +
                                   allgamemodes[gamemode])
            self.display.blit(pressKeySurf, pressKeyRect)

    def drawChooseModePause(self, which):
        whichstring = {0: 'Single Player', 1: 'Battle (two players)',
                       2: 'Coop (two players)'}
        aux = whichstring[which]
        allgamemodes = {'Single Player': 20, 'Battle (two players)': 40,
                        'Coop (two players)': 60}
        for gamemode in allgamemodes:
            if aux == gamemode:
                pressKeySurf = self.basicfont.render(
                    gamemode, True, color.BLUE)
            else:
                pressKeySurf = self.basicfont.render(
                    gamemode, True, color.BLACK)
            pressKeyRect = pressKeySurf.get_rect()
            pressKeyRect.center = (self.window_width/2, self.window_height/2 +
                                   allgamemodes[gamemode])
            self.display.blit(pressKeySurf, pressKeyRect)
