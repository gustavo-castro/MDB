#Mecanismos de Batalha

import random, pygame, sys
from pygame.locals import *
import characters
import ts
import objects
from utils import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
BACKGROUND= (247, 253, 189)
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, FONT, NAME, ImagesPlayer, ImagesEnemy, newtitlescreen
    NAME = 'Mecanismos de Batalha'
    FONT = 'freesansbold.ttf'

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font(FONT, 18)
    pygame.display.set_caption(NAME)

    ImagesPlayer = loadingimages('ss-mercenaries.png', 'player')
    ImagesEnemy = loadingimages('ss-mercenaries.png', 'enemy')

    newtitlescreen = ts.TitleScreen(DISPLAYSURF, BASICFONT, FPSCLOCK, FPS, WINDOWWIDTH, WINDOWHEIGHT)
    showStartScreen()
    while True:
        lost = runGame()
        if lost:
            showGameOverScreen()
        else:
            showWinnerScreen()

def terminate():
    pygame.quit()
    sys.exit()

def showStartScreen():
    newtitlescreen.drawStartScreen()
    pygame.display.update()
    running = True
    while running: # menu key handler
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                terminate()
            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                pygame.event.get() #clear queue
                running = False
                break

def showGameOverScreen():
    newtitlescreen.drawGameOverScreen()
    pygame.display.update()
    pygame.time.wait(1000)
    pygame.event.get()
    running = True
    while running: # menu key handler
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                terminate()
            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                pygame.event.get() #clear queue
                running = False
                break

def showWinnerScreen():
    newtitlescreen.drawWinnerScreen()
    pygame.display.update()
    pygame.time.wait(1000)
    pygame.event.get()
    running = True
    while running: # menu key handler
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                terminate()
            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                pygame.event.get() #clear queue
                running = False
                break

def showPauseScreen():
    newtitlescreen.drawPauseScreen()
    pygame.display.update()
    pygame.time.wait(1000)
    pygame.event.get()
    running = True
    while running: # menu key handler
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                terminate()
            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                pygame.event.get() #clear queue
                running = False
                break

def runGame():
    # Group for drawing all sprites
    rendergroup = pygame.sprite.RenderPlain()
    # Initiate main character
    player_list = pygame.sprite.Group()
    Marcus = characters.Player('Marcus', ImagesPlayer, WINDOWWIDTH, WINDOWHEIGHT, CELLSIZE, rendergroup)
    Marcus.add(player_list, rendergroup)

    friendly_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()
    
    # Create enemies
    N = 3
    enemy_list = createenemies(N, ImagesEnemy, Marcus, WINDOWWIDTH, WINDOWHEIGHT, CELLSIZE, rendergroup)

    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = createwalls(WINDOWWIDTH, WINDOWHEIGHT, rendergroup)
    Marcus.walls = wall_list

    while (not Marcus.dead) and len(enemy_list.sprites()) > 0: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                showPauseScreen()
            elif event.type == KEYDOWN and event.key == K_r:
                Marcus.reload()
            elif event.type == KEYDOWN:
                Marcus.updatePosition(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                Marcus.shoot(friendly_bullet_list, rendergroup)

        Marcus.updatedirection()

        player_list.update()
        enemy_list.update(enemy_bullet_list, rendergroup)
        
        for i in range(10):
            friendly_bullet_list.update(enemy_list, wall_list)
            enemy_bullet_list.update(player_list, wall_list)

        DISPLAYSURF.fill(BACKGROUND)
        rendergroup.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    return Marcus.dead

if __name__ == '__main__':
    main()