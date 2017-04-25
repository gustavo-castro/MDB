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

def runGame():
    contbullet = 1

    # Initiate main character
    all_sprites_list = pygame.sprite.Group()
    Marcus = characters.Player('Marcus', ImagesPlayer, all_sprites_list, WINDOWWIDTH, WINDOWHEIGHT, CELLSIZE)

    all_sprites_list.add(Marcus)
    enemy_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    bullet_enemy_list = pygame.sprite.Group()

    N = 1
    createenemies(N, WINDOWWIDTH, WINDOWHEIGHT, enemy_list, all_sprites_list, ImagesEnemy, CELLSIZE)

    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = createwalls(WINDOWWIDTH, WINDOWHEIGHT, all_sprites_list)
    Marcus.walls = wall_list

    while (not Marcus.dead) and len(enemy_list.sprites()) > 0: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                terminate()
            elif event.type == KEYDOWN:
                Marcus.updatePosition(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                createbullet(Marcus, bullet_list, all_sprites_list)

        Marcus.updatedirection()
        
        createenemybullet(Marcus, enemy_list, bullet_enemy_list, all_sprites_list, contbullet)

        hitenemybullets(bullet_enemy_list, Marcus, all_sprites_list)
        hitbullets(bullet_list, enemy_list, Marcus.walls, all_sprites_list)

        all_sprites_list.update()
        DISPLAYSURF.fill(BACKGROUND)
        all_sprites_list.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        contbullet += 1
        if contbullet == 5: contbullet = 0
    return Marcus.dead

if __name__ == '__main__':
    main()