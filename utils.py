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

    wallsize = screen.cellsize
    
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
    barriersize = screen.cellsize*3
    wall = objects.Wall(40, 60, 50, barriersize)
    wall.add(wall_list, rendergroup)

    wall = objects.Wall(screen.width - 60, screen.height - 60, barriersize/3, 20, tallwall = False)
    wall.add(wall_list, rendergroup)

    wall = objects.Wall(50, screen.height - 80, 40, barriersize)
    wall.add(wall_list, rendergroup)

    return wall_list


def createenemies(N, ImagesDict, player_list, screen, rendergroup, walls):
    """spawns N enemies"""
    enemy_list = pygame.sprite.Group()
    enemy_counter = 0

    while enemy_counter < N:
        enemy = characters.Enemy(ImagesDict, player_list, screen, rendergroup, walls)

        if not pygame.sprite.spritecollide(enemy, enemy_list, False): #only add enemies if there's no collision with other enemies
            enemy.add(enemy_list, rendergroup)
            enemy_counter += 1
    
    return enemy_list

def loadingimages(image, who, cellsize):
    ss = spritesheet.spritesheet(image)
    # Sprite is 16x16 pixels at location 0,0 in the file...
    #olhando pra cada direcao
    if who == 'player':
        d = [ss.image_at((8 + 40*i, 182, cellsize*6, cellsize*7)) for i in range(6)]
        r = [ss.image_at((6 + 40*i, 104, cellsize*6, cellsize*7)) for i in range(6)]
        l = [ss.image_at((10 + 40*i, 264, cellsize*6, cellsize*7)) for i in range(6)]
        u = [ss.image_at((8 + 40*i, 22, cellsize*6, cellsize*7)) for i in range(6)]
        dr = [ss.image_at((6 + 40*i, 142, cellsize*6, cellsize*7)) for i in range(6)]
        dl = [ss.image_at((10 + 40*i, 222, cellsize*6, cellsize*7)) for i in range(6)]
        ur = [ss.image_at((8 + 40*i, 62, cellsize*6, cellsize*7)) for i in range(6)]
        ul = [ss.image_at((2, 304, cellsize*6, cellsize*7)), ss.image_at((60, 304, cellsize*6, cellsize*7)),
        ss.image_at((90, 304, cellsize*6, cellsize*7)), ss.image_at((134, 304, cellsize*6, cellsize*7)),
        ss.image_at((172, 304, cellsize*6, cellsize*7)), ss.image_at((202, 304, cellsize*6, cellsize*7))]
        cd = [ss.image_at((90, 184, cellsize*5, cellsize*4)),0,0,0,0,ss.image_at((210, 184, cellsize*5, cellsize*4))]
        cr = [ss.image_at((90, 104, cellsize*5, cellsize*5)),0,0,0,0,ss.image_at((210, 104, cellsize*5, cellsize*5))]
        cl = [ss.image_at((90, 264, cellsize*5, cellsize*5)),0,0,0,0,ss.image_at((210, 264, cellsize*5, cellsize*5))]
        cu = [ss.image_at((91, 22, cellsize*5, cellsize*4)),0,0,0,0,ss.image_at((211, 22, cellsize*5, cellsize*4))]
        cdr = [ss.image_at((206, 142, cellsize*5, cellsize*5)), ss.image_at((206, 142, cellsize*5, cellsize*4))]
        cdl = [ss.image_at((214, 222, cellsize*5, cellsize*5)), ss.image_at((214, 222, cellsize*5, cellsize*4))]
        cur = [ss.image_at((212, 62, cellsize*5, cellsize*5)), ss.image_at((212, 62, cellsize*5, cellsize*4))]
        cul = [ss.image_at((202, 304, cellsize*5, cellsize*5)), ss.image_at((202, 304, cellsize*5, cellsize*4))]
        ImagesDict = {'d' : d, 'u' : u, 'r' : r, 'l' : l, 'dr' : dr, 'dl' : dl, 'ur' : ur, 'ul' : ul, 'cd' : cd,
        'cr' : cr, 'cu' : cu, 'cl' : cl, 'cdr' : cdr, 'cdl' : cdl, 'cur' : cur, 'cul' : cul}
    elif who == 'enemy':
        d = [ss.image_at((258 + 40*i, 182, cellsize*6, cellsize*7)) for i in range(6)]
        r = [ss.image_at((260 + 40*i, 104, cellsize*6, cellsize*7)) for i in range(6)]
        l = [ss.image_at((256 + 40*i, 262, cellsize*6, cellsize*7)) for i in range(6)]
        u = [ss.image_at((258 + 40*i, 22, cellsize*6, cellsize*7)) for i in range(6)]
        dr = [ss.image_at((260 + 40*i, 142, cellsize*6, cellsize*7)) for i in range(6)]
        dl = [ss.image_at((258 + 40*i, 222, cellsize*6, cellsize*7)) for i in range(6)]
        ur = [ss.image_at((258 + 40*i, 60, cellsize*6, cellsize*7)) for i in range(6)]
        ul = [ss.image_at((258 + 40*i, 302, cellsize*6, cellsize*7)) for i in range(6)]
        ImagesDict = {'d' : d, 'u' : u, 'r' : r, 'l' : l, 'dr' : dr, 'dl' : dl, 'ur' : ur, 'ul' : ul}

    return ImagesDict