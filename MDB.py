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
    global FPSCLOCK, DISPLAYSURF, BASICFONT, FONT, NAME, MarcusImage, ImagesPlayer, ImagesEnemy
    NAME = 'Mecanismos de Batalha'
    FONT = 'freesansbold.ttf'

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font(FONT, 18)
    pygame.display.set_caption(NAME)

    ImagesPlayer = loadingimages('ss-mercenaries.png', 'player')
    ImagesEnemy = loadingimages('ss-mercenaries.png', 'enemy')

    newtitlescreen = ts.TitleScreen()
    newtitlescreen.showStartScreen(DISPLAYSURF, BASICFONT, FPSCLOCK)
    while True:
        runGame()
        newtitlescreen.showGameOverScreen()

def terminate():
    pygame.quit()
    sys.exit()

def runGame():
    # Initiate main character
    all_sprites_list = pygame.sprite.Group()
    Marcus = characters.Character('Marcus', ImagesPlayer, all_sprites_list)

    all_sprites_list.add(Marcus)
    enemy_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()

    N = 10
    createenemies(N, WINDOWWIDTH, WINDOWHEIGHT, enemy_list, all_sprites_list, ImagesEnemy)

    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = createwalls(WINDOWWIDTH, WINDOWHEIGHT, all_sprites_list)
    Marcus.walls = wall_list

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                Marcus.updatePosition(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                createbullet(Marcus, bullet_list, all_sprites_list)

        Marcus.updatedirection()
        
        hitbullets(bullet_list, enemy_list, Marcus.walls, all_sprites_list)

        all_sprites_list.update()
        DISPLAYSURF.fill(BACKGROUND)
        all_sprites_list.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()