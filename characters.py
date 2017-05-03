import random, pygame, math
from pygame.locals import *
import lifebar
import objects
import bulletsprite

class Character(pygame.sprite.Sprite):
    def __init__(self, name, imagedict, hp, window_width, window_height, cellsize, rendergroup):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.imagedict = imagedict
        self.image = self.imagedict['down']
        self.rect = self.image.get_rect()
        self.walls = None
        self.hp = hp
        self.totalhp = hp
        self.lifebar = lifebar.Lifebar(self)
        rendergroup.add(self.lifebar)
        self.cellsize = cellsize
        [self.x, self.y] = self.spawn(window_width, window_height)
        self.rect.center = (self.x, self.y)

    def updatePosition(self, eventkey):
        aux = 0
        if (eventkey == K_a):
            self.x -= self.cellsize
            self.rect.x = self.x
            self.image = self.imagedict['left']
            aux = 1
        elif (eventkey == K_d):
            self.x += self.cellsize
            self.rect.x = self.x
            self.image = self.imagedict['right']
            aux = 2
        elif (eventkey == K_w):
            self.y -= self.cellsize
            self.rect.y = self.y
            self.image = self.imagedict['up']
            aux = 3
        elif (eventkey == K_s):
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
        [x, y] = pygame.mouse.get_pos()
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

    def spawn(self, window_width, window_height):
        raise NotImplementedError

    def update(self):
        self.lifebar.update()

class Player(Character):
    def __init__(self, name, imagedict, window_width, window_height, cellsize, rendergroup):
        Character.__init__(self, name, imagedict, 10.,window_width, window_height, cellsize, rendergroup)
        self.dead = False
        self.totalammo = 10.
        self.ammo = 10.        
        self.bulletsprite = bulletsprite.BulletSprite(self)
        rendergroup.add(self.bulletsprite)
        self.reloadCountdown = 0

    def spawn(self, window_width, window_height):
        return [random.randint(23,window_width-23),random.randint(32, window_height/2 - 32)]        

    def shoot(self, friendly_bullet_list, rendergroup):
        """shoots a bullet where the mouse is pointed if there is ammo"""
        if self.ammo == 0 : return

        bullet = objects.FriendlyBullet(pygame.mouse.get_pos(), [self.rect.centerx, self.rect.centery])

        bullet.add(friendly_bullet_list, rendergroup)

        self.ammo -= 1

    def killhim(self):
        self.dead = True
        self.kill()

    def draw(self):
        print("oxe")

    def reload(self):
        """sets the clock for reloading"""
        self.reloadCountdown = 10

    def update(self):
        Character.update(self)
        if self.reloadCountdown == 1:
            self.reloadCountdown = 0
            self.ammo = 10.
        elif self.reloadCountdown > 1:
            self.reloadCountdown -= 1
        self.bulletsprite.update()


class Enemy(Character):
    count = 0

    def __init__(self, imagedict, player_list, window_width, window_height, cellsize, rendergroup):
        Character.__init__(self, "enemy" + str(Enemy.count), imagedict, 5., window_width, window_height, cellsize, rendergroup)
        Enemy.count += 1
        self.contbullet = 5
        self.auxbullet = 0
        self.player_list = player_list

    def spawn(self, window_height, window_width):
        return [random.randint(27,window_width-27),random.randint(window_height/2+34, window_height-5*34)]

    def shoot(self, enemy_bullet_list, rendergroup):
        """shoots a bullet at the player"""
        dist = float('inf')
        for player in self.player_list.sprites():
            tempdist = (player.rect.centerx - self.rect.centerx)**2 + (player.rect.centery - self.rect.centery)**2
            if tempdist < dist:
                dist = tempdist
                closestplayer = player
        bullet = objects.EnemyBullet([closestplayer.rect.centerx, closestplayer.rect.centery], [self.rect.centerx, self.rect.centery])
        bullet.add(enemy_bullet_list, rendergroup)

    def killhim(self):
        self.kill()

    def update(self, enemy_bullet_list, rendergroup):
        Character.update(self)
        if self.auxbullet == self.contbullet:
            self.shoot(enemy_bullet_list, rendergroup)
            self.auxbullet = 0
        self.auxbullet += 1