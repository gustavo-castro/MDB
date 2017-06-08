import random, pygame, math
from pygame.locals import *
import lifebar
import objects
import bulletsprite

class Character(pygame.sprite.Sprite):
    def __init__(self, name, imagedict, hp, screen, rendergroup):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.feetleft = True
        self.feettonum = {True : 2, False : 4}
        self.imagedict = imagedict
        self.currentdirection = 'd'
        self.image = self.imagedict[self.currentdirection][2]
        self.imageshoot = self.image
        self.shot = 0
        self.rect = self.image.get_rect()
        self.walls = None
        self.hp = hp
        self.totalhp = hp
        self.lifebar = lifebar.Lifebar(self)
        rendergroup.add(self.lifebar)
        self.cellsize = screen.cellsize
        self.walksize_x = self.cellsize*4
        self.walksize_y = self.cellsize*4
        self.screen = screen
        [self.x, self.y] = self.spawn()
        self.rect.x = self.x
        self.rect.y = self.y
        self.cover = False
        self.auxangle = 6

    def updatePosition(self, eventkey):
        aux = 0
        if (eventkey == K_a):
            self.x -= self.walksize_x
            self.rect.x = self.x
            self.feetleft = not self.feetleft
            self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
            self.cover = False
            aux = 1
        elif (eventkey == K_d):
            self.x += self.walksize_x
            self.rect.x = self.x
            self.feetleft = not self.feetleft
            self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
            self.cover = False
            aux = 2
        elif (eventkey == K_w):
            self.y -= self.walksize_y
            self.rect.y = self.y
            self.feetleft = not self.feetleft
            self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
            self.cover = False
            aux = 3
        elif (eventkey == K_s):
            self.y += self.walksize_y
            self.rect.y = self.y
            self.feetleft = not self.feetleft
            self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
            self.cover = False
            aux = 4
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        if block_hit_list:
            if aux == 1:
                self.x += self.walksize_x
                self.rect.x = self.x
                self.cover = True
                self.image = self.imagedict['cr']
            elif aux == 2:
                self.x -= self.walksize_x
                self.rect.x = self.x
                self.cover = True
                self.image = self.imagedict['cl']
            elif aux == 3:
                self.y += self.walksize_y
                self.rect.y = self.y
                self.cover = True
                self.image = self.imagedict['cd']
            elif aux == 4:
                self.y -= self.walksize_y
                self.rect.y = self.y
                self.cover = True
                self.image = self.imagedict['cu']

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
        if auxangle == self.auxangle: return
        else:
            self.auxangle = auxangle
            if auxangle == 1:
                self.currentdirection = 'r'
                self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
            elif auxangle == 2:
                self.currentdirection = 'ur'
                self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
            elif auxangle == 3:
                self.currentdirection = 'u'
                self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
            elif auxangle == 4:
                self.currentdirection = 'ue'
                self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
            elif auxangle == 5:
                self.currentdirection = 'dr'
                self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
            elif auxangle == 6:
                self.currentdirection = 'd'
                self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
            elif auxangle == 7:
                self.currentdirection = 'de'
                self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
            elif auxangle == 8:
                self.currentdirection = 'l'
                self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]

    def spawn(self):
        raise NotImplementedError

    def update(self):
        self.lifebar.update()

class Player(Character):
    def __init__(self, name, imagedict, screen, rendergroup):
        Character.__init__(self, name, imagedict, 10., screen, rendergroup)
        self.dead = False
        self.totalammo = 10.
        self.ammo = 10.        
        self.bulletsprite = bulletsprite.BulletSprite(self)
        rendergroup.add(self.bulletsprite)
        self.reloadCountdown = 0

    def spawn(self):
        return [random.randrange(self.cellsize, self.screen.width, self.walksize_x), random.randrange(self.cellsize, self.screen.height, self.walksize_y)]

    def shoot(self, friendly_bullet_list, rendergroup):
        """shoots a bullet where the mouse is pointed if there is ammo"""
        if self.ammo == 0 : return

        bullet = objects.FriendlyBullet(pygame.mouse.get_pos(), [self.rect.centerx, self.rect.centery])

        bullet.add(friendly_bullet_list, rendergroup)
        self.lastimage = self.image
        self.image = self.imagedict[self.currentdirection][5]
        self.shot = 1

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

    def __init__(self, imagedict, player_list, screen, rendergroup):
        Character.__init__(self, "enemy" + str(Enemy.count), imagedict, 5., screen, rendergroup)
        Enemy.count += 1
        self.contbullet = 5
        self.auxbullet = 0
        self.player_list = player_list

    def spawn(self):
        return [random.randrange(self.cellsize, self.screen.width, self.walksize_x) - self.cellsize*6, random.randrange(self.screen.height/2, self.screen.height, self.walksize_y) - self.cellsize*7]

    def shoot(self, enemy_bullet_list, rendergroup):
        """shoots a bullet at the player"""
        dist = float('inf')
        if self.player_list:
            for player in self.player_list.sprites():
                tempdist = (player.rect.centerx - self.rect.centerx)**2 + (player.rect.centery - self.rect.centery)**2
                if tempdist < dist:
                    dist = tempdist
                    closestplayer = player
            self.updatedirection(closestplayer)
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

    def updatedirection(self, player):
        distance = [player.x - self.x, player.y - self.y]
        angle = -math.atan2(distance[1], distance[0])
        auxangle = self.findquadrant(angle)
        if auxangle == 1:
            self.image = self.imagedict['r'][self.feettonum[self.feetleft]]
        elif auxangle == 2:
            self.image = self.imagedict['ur'][self.feettonum[self.feetleft]]
        elif auxangle == 3:
            self.image = self.imagedict['u'][self.feettonum[self.feetleft]]
        elif auxangle == 4:
            self.image = self.imagedict['ue'][self.feettonum[self.feetleft]]
        elif auxangle == 5:
            self.image = self.imagedict['dr'][self.feettonum[self.feetleft]]
        elif auxangle == 6:
            self.image = self.imagedict['d'][self.feettonum[self.feetleft]]
        elif auxangle == 7:
            self.image = self.imagedict['de'][self.feettonum[self.feetleft]]
        elif auxangle == 8:
            self.image = self.imagedict['l'][self.feettonum[self.feetleft]]
