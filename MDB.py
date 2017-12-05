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
    global newtitlescreen
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

    newtitlescreen = ts.TitleScreen(BASICFONT, FPSCLOCK, SCREEN)
    showStartScreen()
    while True:
        finished = runGame(
            SCREEN, ImagesPlayer, ImagesEnemy, DISPLAYSURF, FPSCLOCK, FPS)
        if finished < 2:
            if runGame == runmultibattle:
                showPlayerWonScreen(finished)
            else:
                if finished == 1:
                    showGameOverScreen()
                elif finished == 0:
                    showWinnerScreen()


def terminate():
    pygame.quit()
    sys.exit()


def showStartScreen():
    which = 0
    directions = {pygame.locals.K_s: 1, pygame.locals.K_DOWN: 1,
                  pygame.locals.K_w: -1, pygame.locals.K_UP: -1}
    whichgamemode = {0: runsingleplayer, 1: runmultibattle, 2: runcoop}
    newtitlescreen.drawStartScreen(which)
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
                newtitlescreen.drawPressChooseModeScreen(which)
                pygame.display.update()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_RETURN:
                global runGame
                runGame = whichgamemode[which]
                running = False
                break


def showGameOverScreen():
    newtitlescreen.drawGameOverScreen()
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


def showWinnerScreen():
    newtitlescreen.drawWinnerScreen()
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


def showPlayerWonScreen(result):
    newtitlescreen.drawBatlleWinnerScreen(result+1)
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


def showChangeMode():
    which = 0
    directions = {pygame.locals.K_s: 1, pygame.locals.K_DOWN: 1,
                  pygame.locals.K_w: -1, pygame.locals.K_UP: -1}
    whichgamemode = {0: runsingleplayer, 1: runmultibattle, 2: runcoop}
    newtitlescreen.drawStartScreen(which)
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
                newtitlescreen.drawPressChooseModeScreen(which)
                pygame.display.update()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_RETURN:
                newmode = whichgamemode[which]
                return newmode


def showPauseScreen():
    which = 0
    directions = {pygame.locals.K_s: 1, pygame.locals.K_DOWN: 1,
                  pygame.locals.K_w: -1, pygame.locals.K_UP: -1}
    newtitlescreen.drawPauseScreen(which)
    pygame.display.update()
    running = True
    while running:  # menu key handler
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT:
                terminate()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key in directions:
                which = (which+directions[event.key]) % 3
                newtitlescreen.drawPauseScreen(which)
                pygame.display.update()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_RETURN:
                running = False
                if which == 0:
                    return 'no changes'
                if which == 1:
                    newmode = showChangeMode()
                    return newmode
                if which == 2:
                    terminate()


def runsingleplayer(
        SCREEN, ImagesPlayer, ImagesEnemy, DISPLAYSURF, FPSCLOCK, FPS):
    # Group for drawing all sprites
    rendergroup = pygame.sprite.RenderPlain()
    wall_list = utils.createwalls(SCREEN, rendergroup)
    # Initiate main character
    player_list = pygame.sprite.Group()

    Marcus = characters.Player('Marcus', ImagesPlayer,
                               SCREEN, rendergroup, wall_list)
    Marcus.add(player_list, rendergroup)

    friendly_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()

    # Create enemies
    N = 2
    enemy_list = utils.createenemies(N, ImagesEnemy, player_list,
                                     SCREEN, rendergroup, wall_list)

    Marcus.other_characters = enemy_list

    while (not Marcus.dead) and len(enemy_list.sprites()) > 0:  # main loop
        if Marcus.movement.shot > 4:
            Marcus.stopshoot()
        elif Marcus.movement.shot > 0:
            Marcus.movement.shot += 1

        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT:
                terminate()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_ESCAPE:
                newmode = showPauseScreen()
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

        if not Marcus.movement.cover and not Marcus.movement.shot:
            Marcus.update_direction()

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


def runmultibattle(
        SCREEN, ImagesPlayer, ImagesEnemy, DISPLAYSURF, FPSCLOCK, FPS):
    # 1v1 battle multiplayer mode
    # Group for drawing all sprites
    rendergroup = pygame.sprite.RenderPlain()
    wall_list = utils.createwalls(SCREEN, rendergroup)
    # Initiate player1
    player_list = pygame.sprite.Group()
    Marcus = characters.Player('Marcus', ImagesPlayer, SCREEN,
                               rendergroup, wall_list)
    Marcus.add(player_list, rendergroup)

    # initiating bullet sprite groups
    friendly_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()

    # Creating player2
    enemy_list = pygame.sprite.Group()
    Cole = characters.Player2('Cole', ImagesPlayer, SCREEN,
                              rendergroup, wall_list)
    while pygame.sprite.spritecollide(Cole, [Marcus], False):
        Cole = characters.Player2('Cole', ImagesPlayer, SCREEN,
                                  rendergroup, wall_list)
    Cole.add(enemy_list, rendergroup)

    Marcus.other_characters = enemy_list
    Cole.other_characters = player_list

    while not Marcus.dead and not Cole.dead:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT:
                terminate()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_ESCAPE:
                newmode = showPauseScreen()
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

        if not Marcus.movement.cover:
            Marcus.update_direction()

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


def runcoop(
        SCREEN, ImagesPlayer, ImagesEnemy, DISPLAYSURF, FPSCLOCK, FPS):
    # Group for drawing all sprites
    rendergroup = pygame.sprite.RenderPlain()
    wall_list = utils.createwalls(SCREEN, rendergroup)
    # Initiate main character
    player_list = pygame.sprite.Group()
    Marcus = characters.Player('Marcus', ImagesPlayer, SCREEN,
                               rendergroup, wall_list)
    Marcus.add(player_list, rendergroup)

    Cole = characters.Player2('Cole', ImagesPlayer, SCREEN,
                              rendergroup, wall_list)
    while pygame.sprite.spritecollide(Cole, [Marcus], False):
        Cole = characters.Player2('Cole', ImagesPlayer, SCREEN,
                                  rendergroup, wall_list)
    Cole.add(player_list, rendergroup)

    friendly_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()

    # Create enemies
    N = 2
    enemy_list = utils.createenemies(N, ImagesEnemy, player_list, SCREEN,
                                     rendergroup, wall_list)

    Marcus.other_characters = enemy_list
    Cole.other_characters = enemy_list

    # main game loop
    while (not Marcus.dead or not Cole.dead) and len(enemy_list.sprites()) > 0:
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.locals.QUIT:
                terminate()
            elif event.type == pygame.locals.KEYDOWN and \
                    event.key == pygame.locals.K_ESCAPE:
                newmode = showPauseScreen()
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

        if not Marcus.movement.cover:
            Marcus.update_direction()

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
