#Mecanismos de Batalha

import random, pygame, sys
from pygame.locals import *
import characters
import ts
import objects

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, FONT, NAME, MarcusImage
    NAME = 'Mecanismos de Batalha'
    FONT = 'freesansbold.ttf'

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font(FONT, 18)
    pygame.display.set_caption(NAME)
    MarcusImage = pygame.image.load('boy.png')

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
    Marcus = characters.Character('Marcus', MarcusImage)

    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(Marcus)
    enemy_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()

    for i in range(10):

        enemy = objects.Enemy(RED)


        enemy.rect.x = random.randrange(WINDOWWIDTH)
        enemy.rect.y = random.randrange(350)

        enemy_list.add(enemy)
        all_sprites_list.add(enemy)

    # Make the walls. (x_pos, y_pos, width, height)
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
    
    Marcus.walls = wall_list

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                Marcus.updatePosition(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                bullet = objects.Bullet(pygame.mouse.get_pos(), [Marcus.x, Marcus.y])

                bullet.rect.x = Marcus.x
                bullet.rect.y = Marcus.y

                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
        
        for bullet in bullet_list:


            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)


            for enemy in enemy_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)


            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

        all_sprites_list.update()
        DISPLAYSURF.fill(WHITE)
        all_sprites_list.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)




if __name__ == '__main__':
    main()