#Mecanismos de Batalha

import random, pygame, sys
from pygame.locals import *
import characters
import mcharacters
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
runGame = 0

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
            elif event.type == KEYDOWN and event.key in {K_s : 0, K_b : 1, K_c : 2}:
                pygame.event.get() #clear queue
                running = False
                if event.key == K_s:
                    global runGame
                    runGame = runsingleplayer
                elif event.key == K_b:
                    global runGame
                    runGame = runmultibattle
                elif event.key == K_c:
                    global runGame
                    runGame = runcoop
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

def runsingleplayer():
    # Group for drawing all sprites
    rendergroup = pygame.sprite.RenderPlain()
    # Initiate main character
    player_list = pygame.sprite.Group()
    Marcus = characters.Player('Marcus', ImagesPlayer, WINDOWWIDTH, WINDOWHEIGHT, CELLSIZE, rendergroup)
    Marcus.add(player_list, rendergroup)

    friendly_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()
    
    # Create enemies
    N = 2
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

def runmultibattle():
    #1v1 battle multiplayer mode
    # Group for drawing all sprites
    rendergroup = pygame.sprite.RenderPlain()
    # Initiate player1
    player_list = pygame.sprite.Group()
    Marcus = characters.Player('Marcus', ImagesPlayer, WINDOWWIDTH, WINDOWHEIGHT, CELLSIZE, rendergroup)
    Marcus.add(player_list, rendergroup)

    #initiating bullet sprite groups
    friendly_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()
    
    # Creating player2
    enemy_list = pygame.sprite.Group()
    Cole = mcharacters.Player('Cole', ImagesPlayer, WINDOWWIDTH, WINDOWHEIGHT, CELLSIZE, rendergroup)
    Cole.add(enemy_list, rendergroup)

    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = createwalls(WINDOWWIDTH, WINDOWHEIGHT, rendergroup)
    Marcus.walls = wall_list
    Cole.walls = wall_list

    while (not Marcus.dead and not Cole.dead): # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                showPauseScreen()
            elif event.type == KEYDOWN and event.key == K_r:
                Marcus.reload()
            elif event.type == KEYDOWN and event.key == K_k:
                Cole.reload()
            elif event.type == KEYDOWN and event.key == K_l:
                Cole.shoot(enemy_bullet_list, rendergroup)
            elif event.type == KEYDOWN:
                Marcus.updatePosition(event.key)
                Cole.updatePosition(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                Marcus.shoot(friendly_bullet_list, rendergroup)

        Marcus.updatedirection()

        player_list.update()
        enemy_list.update()
        
        for i in range(10):
            friendly_bullet_list.update(enemy_list, wall_list)
            enemy_bullet_list.update(player_list, wall_list)

        DISPLAYSURF.fill(BACKGROUND)
        rendergroup.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    return Marcus.dead or Cole.dead

def runcoop():
    # Group for drawing all sprites
    rendergroup = pygame.sprite.RenderPlain()
    # Initiate main character
    player_list = pygame.sprite.Group()
    Marcus = characters.Player('Marcus', ImagesPlayer, WINDOWWIDTH, WINDOWHEIGHT, CELLSIZE, rendergroup)
    Marcus.add(player_list, rendergroup)

    Cole = mcharacters.Player('Cole', ImagesPlayer, WINDOWWIDTH, WINDOWHEIGHT, CELLSIZE, rendergroup)
    Cole.add(player_list, rendergroup)

    friendly_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()
    
    # Create enemies
    N = 2
    enemy_list = createenemies(N, ImagesEnemy, player_list, WINDOWWIDTH, WINDOWHEIGHT, CELLSIZE, rendergroup)

    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = createwalls(WINDOWWIDTH, WINDOWHEIGHT, rendergroup)
    Marcus.walls = wall_list
    Cole.walls = wall_list

    while (not Marcus.dead or not Cole.dead) and len(enemy_list.sprites()) > 0: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                showPauseScreen()
            elif event.type == KEYDOWN and event.key == K_r:
                Marcus.reload()
            elif event.type == KEYDOWN and event.key == K_k:
                Cole.reload()
            elif event.type == KEYDOWN and event.key == K_l:
                Cole.shoot(friendly_bullet_list, rendergroup)
            elif event.type == KEYDOWN:
                Marcus.updatePosition(event.key)
                Cole.updatePosition(event.key)
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
    return Marcus.dead and Cole.dead

if __name__ == '__main__':
    main()