import pygame, random
import objects

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
     
    wall = objects.Wall(0, 0, 10, WINDOWHEIGHT)
    wall_list.add(wall)
    all_sprites_list.add(wall)
     
    wall = objects.Wall(10, 0, WINDOWWIDTH, 10)
    wall_list.add(wall)
    all_sprites_list.add(wall)
     
    wall = objects.Wall(10, WINDOWHEIGHT - 10, WINDOWWIDTH, 10)
    wall_list.add(wall)
    all_sprites_list.add(wall)

    wall = objects.Wall(WINDOWWIDTH - 10, 10, 10, WINDOWHEIGHT)
    wall_list.add(wall)
    all_sprites_list.add(wall)

    return wall_list

def createenemies(N, WINDOWWIDTH, WINDOWHEIGHT, enemy_list, all_sprites_list):
    """spawns N enemies"""
    for i in range(N):

        enemy = objects.Enemy(RED)


        enemy.rect.x = random.randrange(WINDOWWIDTH)
        enemy.rect.y = random.randrange(WINDOWHEIGHT)

        enemy_list.add(enemy)
        all_sprites_list.add(enemy)