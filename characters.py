import random, pygame, math
from pygame.locals import *
import utils

class Character(pygame.sprite.Sprite):
    def __init__(self, name, imagedict, all_sprites_list, hp, cellsize):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.imagedict = imagedict
        self.image = self.imagedict['down']
        self.rect = self.image.get_rect()
        self.walls = None
        self.hp = hp
        self.totalhp = hp
        self.hpbar = utils.Livebar(self)
        all_sprites_list.add(self.hpbar)
        self.cellsize = cellsize

    def updatePosition(self, eventkey):
        aux = 0
        if (eventkey == K_LEFT or eventkey == K_a):
            self.x -= self.cellsize
            self.rect.x = self.x
            self.image = self.imagedict['left']
            aux = 1
        elif (eventkey == K_RIGHT or eventkey == K_d):
            self.x += self.cellsize
            self.rect.x = self.x
            self.image = self.imagedict['right']
            aux = 2
        elif (eventkey == K_UP or eventkey == K_w):
            self.y -= self.cellsize
            self.rect.y = self.y
            self.image = self.imagedict['up']
            aux = 3
        elif (eventkey == K_DOWN or eventkey == K_s):
            self.y += self.cellsize
            self.rect.y = self.y
            self.image = self.imagedict['down']
            aux = 4
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        if block_hit_list:
            if aux == 1:
                self.x += self.cellsize
                self.rect.x = self.x
            elif aux == 2:
                self.x -= self.cellsize
                self.rect.x = self.x
            elif aux == 3:
                self.y += self.cellsize
                self.rect.y = self.y
            elif aux == 4:
                self.y -= self.cellsize
                self.rect.y = self.y

    def findquadrant(self, angle):
        pi = math.pi
        #r
        if angle > -pi/8 and angle <= pi/8:
            return 1
        #ur
        elif angle > pi/8 and angle <= 3*pi/8:
            return 2
        #u
        elif angle > 3*pi/8 and angle <= 5*pi/8:
            return 3
        #ue
        elif angle > 5*pi/8 and angle <= 7*pi/8:
            return 4
        #dr
        elif angle <= -pi/8 and angle > -3*pi/8:
            return 5
        #d
        elif angle <= -3*pi/8 and angle > -5*pi/8:
            return 6
        #de
        elif angle <= -5*pi/8 and angle > -7*pi/8:
            return 7
        #e
        else:
            return 8

    def updatedirection(self):
        mouse = pygame.mouse.get_pos()
        x = mouse[0]
        y = mouse[1]
        distance = [x - self.x, y - self.y]
        angle = -math.atan2(distance[1], distance[0])
        auxangle = self.findquadrant(angle)
        if auxangle == 1:
            self.image = self.imagedict['right']
        elif auxangle == 2:
            self.image = self.imagedict['ur']
        elif auxangle == 3:
            self.image = self.imagedict['up']
        elif auxangle == 4:
            self.image = self.imagedict['ue']
        elif auxangle == 5:
            self.image = self.imagedict['dr']
        elif auxangle == 6:
            self.image = self.imagedict['down']
        elif auxangle == 7:
            self.image = self.imagedict['de']
        elif auxangle == 8:
            self.image = self.imagedict['left']

class Player(Character):
    def __init__(self, name, imagedict, all_sprites_list, window_width, window_height, cellsize):
        Character.__init__(self, name, imagedict, all_sprites_list, 10., cellsize)

        start = self.spawnplayer(window_width, window_height)
        self.x = start[0]
        self.y = start[1]
        self.rect.x = self.x
        self.rect.y = self.y
        self.dead = False

    def spawnplayer(self, window_width, window_height):
        return [random.randrange(window_width),random.randint(0, window_height/2)]

    def killhim(self):
        self.dead = True
        self.kill()


class Enemy(Character):
    count = 0

    def __init__(self, imagedict, all_sprites_list, window_width, window_height, cellsize):
        Character.__init__(self, "enemy" + str(Enemy.count), imagedict, all_sprites_list, 5., cellsize)
        Enemy.count += 1

        start = self.spawnenemy(window_width, window_height)
        self.x = start[0]
        self.y = start[1]
        self.rect.x = self.x
        self.rect.y = self.y

    def spawnenemy(self, window_width, window_height):
        return [random.randrange(window_width),random.randint(window_height/2, window_height)]

    def killhim(self):
        self.kill()