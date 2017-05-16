import pygame
import spritesheet
import objects
import characters

class Screen(object):
    def __init__(self, window_width, window_height, cellsize, fps, display):
        self.width = window_width
        self.height = window_height
        self.cellsize = cellsize
        self.fps = fps
        self.display = display

def createwalls(screen, rendergroup):
    """creates walls for the basic level """
    wall_list = pygame.sprite.Group()

    wallsize = 1
    
    """outside walls"""
    wall = objects.Wall(0, 0, wallsize, screen.height)
    wall.add(wall_list, rendergroup)
     
    wall = objects.Wall(wallsize, 0, screen.width, wallsize)
    wall.add(wall_list, rendergroup)
     
    wall = objects.Wall(wallsize, screen.height - wallsize, screen.width, wallsize)
    wall.add(wall_list, rendergroup)

    wall = objects.Wall(screen.width - wallsize, wallsize, wallsize, screen.height)
    wall.add(wall_list, rendergroup)

    """barriers in the middle of the level"""
    barriersize = 15
    wall = objects.Wall(40, 60, 50, barriersize)
    wall.add(wall_list, rendergroup)

    wall = objects.Wall(screen.width - 60, screen.height - 60, barriersize/3, 30, tallwall = False)
    wall.add(wall_list, rendergroup)

    wall = objects.Wall(50, screen.height - 70, 40, barriersize)
    wall.add(wall_list, rendergroup)

    return wall_list


def createenemies(N, ImagesDict, player_list, screen, rendergroup):
    """spawns N enemies"""
    enemy_list = pygame.sprite.Group()

    for i in range(N):
        enemy = characters.Enemy(ImagesDict, player_list, screen, rendergroup)

        enemy.add(enemy_list, rendergroup)
    
    return enemy_list

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
        ue = [ss.image_at((6, 304, 23, 32)), ss.image_at((54, 304, 23, 32)),
        ss.image_at((94, 304, 23, 32)), ss.image_at((138, 304, 23, 32)), ss.image_at((176, 304, 23, 32)), ss.image_at((206, 304, 23, 32))]
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