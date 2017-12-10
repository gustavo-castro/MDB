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

    wall = objects.Wall(wallsize, screen.height - wallsize,
                        screen.width, wallsize)
    wall.add(wall_list, rendergroup)

    wall = objects.Wall(screen.width - wallsize, wallsize,
                        wallsize, screen.height)
    wall.add(wall_list, rendergroup)

    """barriers in the middle of the level"""
    ss = spritesheet.spritesheet('Images/Walls.png')
    wall = objects.Wall(40, 60, 60, 30, image=ss.image_at((122, 146, 60, 30)))
    wall.add(wall_list, rendergroup)

    wall = objects.Wall(screen.width - 100, screen.height - 120, 15, 60,
                        image=ss.image_at((121, 65, 15, 60)), tallwall=False)
    wall.add(wall_list, rendergroup)

    wall = objects.Wall(70, screen.height - 120, 45, 30,
                        ss.image_at((122, 146, 45, 30)))
    wall.add(wall_list, rendergroup)

    return wall_list


def createenemies(N, ImagesDict, player_list, screen, rendergroup, walls,
                  enemy_list):
    """spawns N enemies"""
    for i in range(N):
        characters.Enemy(ImagesDict, player_list, screen,
                         rendergroup, walls, enemy_list)

    return


def loadingimages(image, who, cellsize):
    ss = spritesheet.spritesheet(image)
    # Sprite is 16x16 pixels at location 0,0 in the file...
    # Looking at every direction
    if who == 'player':
        d = [ss.image_at((8 + 40*i, 182, cellsize*6, cellsize*7))
             for i in [2, 4, 5]]
        d = {image_type: image for (image_type, image)
             in zip(["left", "right", "shoot"], d)}
        r = [ss.image_at((6 + 40*i, 104, cellsize*6, cellsize*7))
             for i in [2, 4, 5]]
        r = {image_type: image for (image_type, image)
             in zip(["left", "right", "shoot"], r)}
        left = [ss.image_at((10 + 40*i, 264, cellsize*6, cellsize*7))
                for i in [2, 4, 5]]
        left = {image_type: image for (image_type, image)
                in zip(["left", "right", "shoot"], left)}
        u = [ss.image_at((8 + 40*i, 22, cellsize*6, cellsize*7))
             for i in [2, 4, 5]]
        u = {image_type: image for (image_type, image)
             in zip(["left", "right", "shoot"], u)}
        dr = [ss.image_at((6 + 40*i, 142, cellsize*6, cellsize*7))
              for i in [2, 4, 5]]
        dr = {image_type: image for (image_type, image)
              in zip(["left", "right", "shoot"], dr)}
        dl = [ss.image_at((10 + 40*i, 222, cellsize*6, cellsize*7))
              for i in [2, 4, 5]]
        dl = {image_type: image for (image_type, image)
              in zip(["left", "right", "shoot"], dl)}
        ur = [ss.image_at((8 + 40*i, 62, cellsize*6, cellsize*7))
              for i in [2, 4, 5]]
        ur = {image_type: image for (image_type, image)
              in zip(["left", "right", "shoot"], ur)}
        ul = [ss.image_at((90, 304, cellsize*6, cellsize*7)),
              ss.image_at((172, 304, cellsize*6, cellsize*7)),
              ss.image_at((202, 304, cellsize*6, cellsize*7))]
        ul = {image_type: image for (image_type, image)
              in zip(["left", "right", "shoot"], ul)}
        cd = [ss.image_at((90, 184, cellsize*5, cellsize*4)),
              ss.image_at((210, 184, cellsize*5, cellsize*4))]
        cd = {image_type: image for (image_type, image)
              in zip(["cover", "shoot"], cd)}
        cr = [ss.image_at((90, 104, cellsize*5, cellsize*5)),
              ss.image_at((210, 104, cellsize*5, cellsize*5))]
        cr = {image_type: image for (image_type, image)
              in zip(["cover", "shoot"], cr)}
        cl = [ss.image_at((90, 264, cellsize*5, cellsize*5)),
              ss.image_at((210, 264, cellsize*5, cellsize*5))]
        cl = {image_type: image for (image_type, image)
              in zip(["cover", "shoot"], cl)}
        cu = [ss.image_at((91, 22, cellsize*5, cellsize*4)),
              ss.image_at((211, 22, cellsize*5, cellsize*4))]
        cu = {image_type: image for (image_type, image)
              in zip(["cover", "shoot"], cu)}
        cdr = [ss.image_at((206, 142, cellsize*5, cellsize*5)),
               ss.image_at((206, 142, cellsize*5, cellsize*4))]
        cdr = {image_type: image for (image_type, image)
               in zip(["left", "right"], cdr)}
        cdl = [ss.image_at((214, 222, cellsize*5, cellsize*5)),
               ss.image_at((214, 222, cellsize*5, cellsize*4))]
        cdl = {image_type: image for (image_type, image)
               in zip(["left", "right"], cdl)}
        cur = [ss.image_at((212, 62, cellsize*5, cellsize*5)),
               ss.image_at((212, 62, cellsize*5, cellsize*4))]
        cur = {image_type: image for (image_type, image)
               in zip(["left", "right"], cur)}
        cul = [ss.image_at((202, 304, cellsize*5, cellsize*5)),
               ss.image_at((202, 304, cellsize*5, cellsize*4))]
        cul = {image_type: image for (image_type, image)
               in zip(["left", "right"], cul)}
        images_dict = {
            'd': d, 'u': u, 'r': r, 'l': left, 'dr': dr, 'dl': dl, 'ur': ur,
            'ul': ul, 'cd': cd, 'cr': cr, 'cu': cu, 'cl': cl, 'cdr': cdr,
            'cdl': cdl, 'cur': cur, 'cul': cul
        }
    elif who == 'enemy':
        d = [ss.image_at((258 + 40*i, 182, cellsize*6, cellsize*7))
             for i in [2, 4, 5]]
        d = {image_type: image for (image_type, image)
             in zip(["left", "right", "shoot"], d)}
        r = [ss.image_at((260 + 40*i, 104, cellsize*6, cellsize*7))
             for i in [2, 4, 5]]
        r = {image_type: image for (image_type, image)
             in zip(["left", "right", "shoot"], r)}
        left = [ss.image_at((256 + 40*i, 262, cellsize*6, cellsize*7))
                for i in [2, 4, 5]]
        left = {image_type: image for (image_type, image)
                in zip(["left", "right", "shoot"], left)}
        u = [ss.image_at((258 + 40*i, 22, cellsize*6, cellsize*7))
             for i in [2, 4, 5]]
        u = {image_type: image for (image_type, image)
             in zip(["left", "right", "shoot"], u)}
        dr = [ss.image_at((260 + 40*i, 142, cellsize*6, cellsize*7))
              for i in [2, 4, 5]]
        dr = {image_type: image for (image_type, image)
              in zip(["left", "right", "shoot"], dr)}
        dl = [ss.image_at((258 + 40*i, 222, cellsize*6, cellsize*7))
              for i in [2, 4, 5]]
        dl = {image_type: image for (image_type, image)
              in zip(["left", "right", "shoot"], dl)}
        ur = [ss.image_at((258 + 40*i, 60, cellsize*6, cellsize*7))
              for i in [2, 4, 5]]
        ur = {image_type: image for (image_type, image)
              in zip(["left", "right", "shoot"], ur)}
        ul = [ss.image_at((258 + 40*i, 302, cellsize*6, cellsize*7))
              for i in [2, 4, 5]]
        ul = {image_type: image for (image_type, image)
              in zip(["left", "right", "shoot"], ul)}
        images_dict = {'d': d, 'u': u, 'r': r, 'l': left, 'dr': dr, 'dl': dl,
                       'ur': ur, 'ul': ul}

    return images_dict
