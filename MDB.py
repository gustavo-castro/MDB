# Mecanismos de Batalha

import pygame
import sys
import pygame.locals
import characters
import ts
import utils

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 5

BACKGROUND = (247, 253, 189)
runGame = 0


def main():
    NAME = 'Mecanismos de Batalha'
    FONT = 'freesansbold.ttf'
    FPS = 15

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font(FONT, 18)
    pygame.display.set_caption(NAME)
    pygame.key.set_repeat(100)

    ImagesPlayer = utils.loadingimages('Images/ss-mercenaries.png', 'player',
                                       CELLSIZE)
    ImagesEnemy = utils.loadingimages('Images/ss-mercenaries.png', 'enemy',
                                      CELLSIZE)

    SCREEN = utils.Screen(WINDOWWIDTH, WINDOWHEIGHT,
                          CELLSIZE, FPS, DISPLAYSURF)

    titlescreen = ts.TitleScreen(BASICFONT, FPSCLOCK, SCREEN)
    showStartScreen(titlescreen)
    while True:
        finished = runGame(SCREEN, ImagesPlayer, ImagesEnemy,
                           DISPLAYSURF, FPSCLOCK, FPS, titlescreen)
        if finished < 2:
            if runGame == runmultibattle:
                showPlayerWonScreen(finished, titlescreen)
            else:
                if finished == 1:
                    showGameOverScreen(titlescreen)
                elif finished == 0:
                    showWinnerScreen(titlescreen)


def terminate():
    pygame.quit()
    sys.exit()


def showStartScreen(titlescreen):
    which = 0
    directions = {pygame.locals.K_s: 1, pygame.locals.K_DOWN: 1,
                  pygame.locals.K_w: -1, pygame.locals.K_UP: -1}
    whichgamemode = {0: runsingleplayer, 1: runmultibattle, 2: runcoop}
    titlescreen.drawStartScreen(which)
    pygame.display.update()
    running = True
    while running:  # menu key handler
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT or (
                event.type == pygame.locals.KEYDOWN and
                    event.key == pygame.locals.K_ESCAPE):
                terminate()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key in directions:
                which = (which + directions[event.key]) % 3
                titlescreen.drawPressChooseModeScreen(which)
                pygame.display.update()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_RETURN:
                global runGame
                runGame = whichgamemode[which]
                running = False
                break


def showGameOverScreen(titlescreen):
    titlescreen.drawGameOverScreen()
    pygame.display.update()
    pygame.time.wait(1000)
    pygame.event.get()
    running = True
    while running:  # menu key handler
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT or (
                event.type == pygame.locals.KEYDOWN and
                    event.key == pygame.locals.K_ESCAPE):
                terminate()
            elif event.type == pygame.locals.KEYDOWN or \
                    event.type == pygame.locals.MOUSEBUTTONDOWN:
                pygame.event.get()  # clear queue
                running = False
                break


def showWinnerScreen(titlescreen):
    titlescreen.drawWinnerScreen()
    pygame.display.update()
    pygame.time.wait(1000)
    pygame.event.get()
    running = True
    while running:  # menu key handler
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT or (
                event.type == pygame.locals.KEYDOWN and
                    event.key == pygame.locals.K_ESCAPE):
                terminate()
            elif event.type == pygame.locals.KEYDOWN or \
                    event.type == pygame.locals.MOUSEBUTTONDOWN:
                pygame.event.get()  # clear queue
                running = False
                break


def showPlayerWonScreen(result, titlescreen):
    titlescreen.drawBatlleWinnerScreen(result+1)
    pygame.display.update()
    pygame.time.wait(1000)
    pygame.event.get()
    running = True
    while running:  # menu key handler
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT or (
                event.type == pygame.locals.KEYDOWN and
                    event.key == pygame.locals.K_ESCAPE):
                terminate()
            elif event.type == pygame.locals.KEYDOWN or \
                    event.type == pygame.locals.MOUSEBUTTONDOWN:
                pygame.event.get()  # clear queue
                running = False
                break


def showChangeMode(titlescreen):
    which = 0
    directions = {pygame.locals.K_s: 1, pygame.locals.K_DOWN: 1,
                  pygame.locals.K_w: -1, pygame.locals.K_UP: -1}
    whichgamemode = {0: runsingleplayer, 1: runmultibattle, 2: runcoop}
    titlescreen.drawStartScreen(which)
    pygame.display.update()
    while True:  # menu key handler
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT or (
                    event.type == pygame.locals.KEYDOWN and
                    event.key == pygame.locals.K_ESCAPE):
                terminate()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key in directions:
                which = (which+directions[event.key]) % 3
                titlescreen.drawPressChooseModeScreen(which)
                pygame.display.update()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_RETURN:
                newmode = whichgamemode[which]
                return newmode


def showPauseScreen(titlescreen):
    which = 0
    directions = {pygame.locals.K_s: 1, pygame.locals.K_DOWN: 1,
                  pygame.locals.K_w: -1, pygame.locals.K_UP: -1}
    titlescreen.drawPauseScreen(which)
    pygame.display.update()
    running = True
    while running:  # menu key handler
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT:
                terminate()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key in directions:
                which = (which+directions[event.key]) % 3
                titlescreen.drawPauseScreen(which)
                pygame.display.update()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_RETURN:
                running = False
                if which == 0:
                    return 'no changes'
                if which == 1:
                    newmode = showChangeMode(titlescreen)
                    return newmode
                if which == 2:
                    terminate()


def runsingleplayer(SCREEN, ImagesPlayer, ImagesEnemy,
                    DISPLAYSURF, FPSCLOCK, FPS, titlescreen):
    # Group for drawing all sprites
    rendergroup = pygame.sprite.RenderPlain()
    wall_list = utils.createwalls(SCREEN, rendergroup)
    # Initiate main character
    player_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()

    Marcus = characters.Player('Marcus', ImagesPlayer, SCREEN, rendergroup,
                               wall_list, player_list, enemy_list)

    friendly_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()

    # Create enemies
    N = 2
    utils.createenemies(N, ImagesEnemy, player_list, SCREEN,
                        rendergroup, wall_list, enemy_list)

    while (not Marcus.dead) and len(enemy_list.sprites()) > 0:  # main loop
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT:
                terminate()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_ESCAPE:
                newmode = showPauseScreen(titlescreen)
                if newmode != 'no changes':
                    global runGame
                    runGame = newmode
                    return 2
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_r:
                Marcus.reload()
            elif event.type == pygame.locals.KEYDOWN:
                Marcus.update_position(event.key)
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                Marcus.shoot(friendly_bullet_list, rendergroup)

        player_list.update()
        enemy_list.update(enemy_bullet_list, rendergroup)

        for i in range(10):
            friendly_bullet_list.update(enemy_list, wall_list)
            enemy_bullet_list.update(player_list, wall_list)

        DISPLAYSURF.fill(BACKGROUND)
        rendergroup.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    return int(Marcus.dead)


def runmultibattle(SCREEN, ImagesPlayer, ImagesEnemy,
                   DISPLAYSURF, FPSCLOCK, FPS, titlescreen):
    # 1v1 battle multiplayer mode
    # Group for drawing all sprites
    rendergroup = pygame.sprite.RenderPlain()
    wall_list = utils.createwalls(SCREEN, rendergroup)
    # Initiate player1
    player_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()

    Marcus = characters.Player('Marcus', ImagesPlayer, SCREEN, rendergroup,
                               wall_list, player_list, enemy_list)

    # initiating bullet sprite groups
    friendly_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()

    Cole = characters.Player2('Cole', ImagesPlayer, SCREEN, rendergroup,
                              wall_list, player_list, enemy_list, True)

    while not Marcus.dead and not Cole.dead:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT:
                terminate()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_ESCAPE:
                newmode = showPauseScreen(titlescreen)
                if newmode != 'no changes':
                    global runGame
                    runGame = newmode
                    return 2
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_r:
                Marcus.reload()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_k:
                Cole.reload()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_l:
                Cole.shoot(enemy_bullet_list, rendergroup)
            elif event.type == pygame.locals.KEYDOWN:
                Marcus.update_position(event.key)
                Cole.update_position(event.key)
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                Marcus.shoot(friendly_bullet_list, rendergroup)

        player_list.update()
        enemy_list.update()

        for i in range(10):
            friendly_bullet_list.update(enemy_list, wall_list)
            enemy_bullet_list.update(player_list, wall_list)

        DISPLAYSURF.fill(BACKGROUND)
        rendergroup.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    return int(Marcus.dead)


def runcoop(SCREEN, ImagesPlayer, ImagesEnemy,
            DISPLAYSURF, FPSCLOCK, FPS, titlescreen):
    # Group for drawing all sprites
    rendergroup = pygame.sprite.RenderPlain()
    wall_list = utils.createwalls(SCREEN, rendergroup)
    # Initiate main character
    player_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()

    Marcus = characters.Player('Marcus', ImagesPlayer, SCREEN, rendergroup,
                               wall_list, player_list, enemy_list)
    Cole = characters.Player2('Cole', ImagesPlayer, SCREEN, rendergroup,
                              wall_list, player_list, enemy_list, False)

    friendly_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()

    # Create enemies
    N = 2
    utils.createenemies(N, ImagesEnemy, player_list, SCREEN,
                        rendergroup, wall_list, enemy_list)

    # main game loop
    while (not Marcus.dead or not Cole.dead) and len(enemy_list.sprites()) > 0:
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT:
                terminate()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_ESCAPE:
                newmode = showPauseScreen(titlescreen)
                if newmode != 'no changes':
                    global runGame
                    runGame = newmode
                    return 2
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_r:
                Marcus.reload()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_k:
                Cole.reload()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_l:
                Cole.shoot(friendly_bullet_list, rendergroup)
            elif event.type == pygame.locals.KEYDOWN:
                Marcus.update_position(event.key)
                Cole.update_position(event.key)
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                Marcus.shoot(friendly_bullet_list, rendergroup)

        player_list.update()
        enemy_list.update(enemy_bullet_list, rendergroup)

        for i in range(10):
            friendly_bullet_list.update(enemy_list, wall_list)
            enemy_bullet_list.update(player_list, wall_list)

        DISPLAYSURF.fill(BACKGROUND)
        rendergroup.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    return int(Marcus.dead and Cole.dead)


if __name__ == '__main__':
    main()
