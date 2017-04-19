import pygame, random
import objects
import spritesheet

RED       = (255,   0,   0)

def hitbullets(bullet_list, enemy_list, all_sprites_list):
    """checks when bullets hit the enemies"""
    for bullet in bullet_list:

        enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)

        for enemy in enemy_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)


        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

def createbullet(Marcus, bullet_list, all_sprites_list):
    """creates bullets when mouse key is pressed"""
    bullet = objects.Bullet(pygame.mouse.get_pos(), [Marcus.x, Marcus.y])

    bullet.rect.x = Marcus.x
    bullet.rect.y = Marcus.y

    all_sprites_list.add(bullet)
    bullet_list.add(bullet)

def createwalls(WINDOWWIDTH, WINDOWHEIGHT, all_sprites_list):
    """creates walls for the basic level """
    wall_list = pygame.sprite.Group()

    wallsize = 5
     
    wall = objects.Wall(0, 0, wallsize, WINDOWHEIGHT)
    wall_list.add(wall)
    all_sprites_list.add(wall)
     
    wall = objects.Wall(wallsize, 0, WINDOWWIDTH, wallsize)
    wall_list.add(wall)
    all_sprites_list.add(wall)
     
    wall = objects.Wall(wallsize, WINDOWHEIGHT - wallsize, WINDOWWIDTH, wallsize)
    wall_list.add(wall)
    all_sprites_list.add(wall)

    wall = objects.Wall(WINDOWWIDTH - wallsize, wallsize, wallsize, WINDOWHEIGHT)
    wall_list.add(wall)
    all_sprites_list.add(wall)

    return wall_list

def createenemies(N, WINDOWWIDTH, WINDOWHEIGHT, enemy_list, all_sprites_list, ImagesDict):
    """spawns N enemies"""
    for i in range(N):

        enemy = objects.Enemy(ImagesDict)


        enemy.rect.x = random.randrange(WINDOWWIDTH)
        enemy.rect.y = random.randrange(WINDOWHEIGHT)

        enemy_list.add(enemy)
        all_sprites_list.add(enemy)

def loadingimages(image, who):
    ss = spritesheet.spritesheet(image)
    # Sprite is 16x16 pixels at location 0,0 in the file...
    #olhando pra cada direcao
    if who == 'player':
        down = ss.image_at((92, 184, 23, 32))
        right = ss.image_at((90, 104, 23, 32))
        left = ss.image_at((94, 264, 23, 32))
        up = ss.image_at((92, 22, 23, 32))
        dr = ss.image_at((90, 142, 23, 32))
        de = ss.image_at((94, 222, 23, 32))
        ur = ss.image_at((90, 62, 23, 32))
        ue = ss.image_at((96, 304, 23, 32))
        ImagesDict = {'down' : down, 'up' : up, 'right' : right, 'left' : left, 'dr' : dr, 'de' : de, 'ur' : ur, 'ue' : ue}
    elif who == 'enemy':
        down = ss.image_at((338, 182, 27, 34))
        right = ss.image_at((340, 104, 27, 34))
        left = ss.image_at((336, 262, 27, 34))
        up = ss.image_at((338, 22, 27, 34))
        ImagesDict = {'down' : down, 'up' : up, 'right' : right, 'left' : left}

    return ImagesDict