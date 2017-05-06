import pygame
import spritesheet
import objects
import characters

def createwalls(window_width, window_height, rendergroup):
    """creates walls for the basic level """
    wall_list = pygame.sprite.Group()

    wallsize = 1
    barriersize = 5
    
    """outside walls"""
    wall = objects.Wall(0, 0, wallsize, window_height)
    wall.add(wall_list, rendergroup)
     
    wall = objects.Wall(wallsize, 0, window_width, wallsize)
    wall.add(wall_list, rendergroup)
     
    wall = objects.Wall(wallsize, window_height - wallsize, window_width, wallsize)
    wall.add(wall_list, rendergroup)

    wall = objects.Wall(window_width - wallsize, wallsize, wallsize, window_height)
    wall.add(wall_list, rendergroup)

    """barriers in the middle of the level"""
    wall = objects.Wall(40, 60, 50, barriersize)
    wall.add(wall_list, rendergroup)

    wall = objects.Wall(window_width - 60, window_height - 60, 30, barriersize, tallwall = False)
    wall.add(wall_list, rendergroup)

    wall = objects.Wall(50, window_height - 70, 40, barriersize)
    wall.add(wall_list, rendergroup)

    return wall_list


def createenemies(N, ImagesDict, player_list, window_width, window_height, cellsize, rendergroup):
    """spawns N enemies"""
    enemy_list = pygame.sprite.Group()

    for i in range(N):
        enemy = characters.Enemy(ImagesDict, player_list, window_width, window_height, cellsize, rendergroup)

        enemy.add(enemy_list, rendergroup)
    
    return enemy_list

def loadingimages(image, who):
    ss = spritesheet.spritesheet(image)
    # Sprite is 16x16 pixels at location 0,0 in the file...
    #olhando pra cada direcao
    if who == 'player':
        d = ss.image_at((92, 184, 23, 32))
        r = ss.image_at((90, 104, 23, 32))
        l = ss.image_at((94, 264, 23, 32))
        u = ss.image_at((92, 22, 23, 32))
        dr = ss.image_at((90, 142, 23, 32))
        de = ss.image_at((94, 222, 23, 32))
        ur = ss.image_at((90, 62, 23, 32))
        ue = ss.image_at((96, 304, 23, 32))
        ImagesDict = {'d' : d, 'u' : u, 'r' : r, 'l' : l, 'dr' : dr, 'de' : de, 'ur' : ur, 'ue' : ue}
    elif who == 'enemy':
        d = ss.image_at((338, 182, 27, 34))
        r = ss.image_at((340, 104, 27, 34))
        l = ss.image_at((336, 262, 27, 34))
        u = ss.image_at((338, 22, 27, 34))
        dr = ss.image_at((340, 142, 27, 34))
        ur = ss.image_at((338, 60, 27, 34))
        de = ss.image_at((338, 222, 27, 34))
        ue = ss.image_at((338, 302, 27, 34))
        ImagesDict = {'d' : d, 'u' : u, 'r' : r, 'l' : l, 'dr' : dr, 'de' : de, 'ur' : ur, 'ue' : ue}

    return ImagesDict

def loadingimages(image, who):
    ss = spritesheet.spritesheet(image)
    # Sprite is 16x16 pixels at location 0,0 in the file...
    #olhando pra cada direcao
    if who == 'player':
        d = [ss.image_at((12 + 40*i, 182, 23, 32)) for i in range(6)]
        r = [ss.image_at((10 + 40*i, 104, 23, 32)) for i in range(6)]
        l = [ss.image_at((14 + 40*i, 264, 23, 32)) for i in range(6)]
        u = [ss.image_at((12 + 40*i, 22, 23, 32)) for i in range(6)]
        dr = [ss.image_at((10 + 40*i, 142, 23, 32)) for i in range(6)]
        de = [ss.image_at((14 + 40*i, 222, 23, 32)) for i in range(6)]
        ur = [ss.image_at((10 + 40*i, 62, 23, 32)) for i in range(6)]
        ue = [ss.image_at((10 + 40*i, 304, 23, 32)) for i in range(6)]
        ImagesDict = {'d' : d, 'u' : u, 'r' : r, 'l' : l, 'dr' : dr, 'de' : de, 'ur' : ur, 'ue' : ue}
    elif who == 'enemy':
        d = [ss.image_at((258 + 40*i, 182, 27, 34)) for i in range(6)]
        r = [ss.image_at((260 + 40*i, 104, 27, 34)) for i in range(6)]
        l = [ss.image_at((256 + 40*i, 262, 27, 34)) for i in range(6)]
        u = [ss.image_at((258 + 40*i, 22, 27, 34)) for i in range(6)]
        dr = [ss.image_at((260 + 40*i, 142, 27, 34)) for i in range(6)]
        de = [ss.image_at((258 + 40*i, 222, 27, 34)) for i in range(6)]
        ur = [ss.image_at((258 + 40*i, 60, 27, 34)) for i in range(6)]
        ue = [ss.image_at((258 + 40*i, 302, 27, 34)) for i in range(6)]
        ImagesDict = {'d' : d, 'u' : u, 'r' : r, 'l' : l, 'dr' : dr, 'de' : de, 'ur' : ur, 'ue' : ue}

    return ImagesDict