import random, pygame, math
from pygame.locals import *
import lifebar
import objects
import bulletsprite

class mCharacter(pygame.sprite.Sprite):
    """Character implementation using only the keyboard as input (instead of keyboard and mouse), will be used for multiplayer purposes"""
    def __init__(self, name, imagedict, hp, window_width, window_height, cellsize, rendergroup):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.feetleft = True
        self.feettonum = {True : 2, False : 4}
        self.imagedict = imagedict
        self.image = self.imagedict['d'][2]
        self.rect = self.image.get_rect()
        self.walls = None
        self.hp = hp
        self.totalhp = hp
        self.lifebar = lifebar.Lifebar(self)
        rendergroup.add(self.lifebar)
        self.cellsize = cellsize
        [self.x, self.y] = self.spawn(window_width, window_height)
        self.rect.center = (self.x, self.y)
        self.direction = 4
        self.cover = False

    def updatePosition(self, eventkey):
        if (eventkey == K_LEFT):
            self.x -= self.cellsize
            self.rect.x = self.x
            self.image = self.imagedict['l'][self.feettonum[self.feetleft]]
            self.direction = 1
            self.cover = False
        elif (eventkey == K_RIGHT):
            self.x += self.cellsize
            self.rect.x = self.x
            self.image = self.imagedict['r'][self.feettonum[self.feetleft]]
            self.direction = 2
            self.cover = False
        elif (eventkey == K_UP):
            self.y -= self.cellsize
            self.rect.y = self.y
            self.image = self.imagedict['u'][self.feettonum[self.feetleft]]
            self.direction = 3
            self.cover = False
        elif (eventkey == K_DOWN):
            self.y += self.cellsize
            self.rect.y = self.y
            self.image = self.imagedict['d'][self.feettonum[self.feetleft]]
            self.direction = 4
            self.cover = False
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        if block_hit_list:
            if self.direction == 1:
                self.x += self.cellsize
                self.rect.x = self.x
                self.cover = True
            elif self.direction == 2:
                self.x -= self.cellsize
                self.rect.x = self.x
                self.cover = True
            elif self.direction == 3:
                self.y += self.cellsize
                self.rect.y = self.y
                self.cover = True
            elif self.direction == 4:
                self.y -= self.cellsize
                self.rect.y = self.y
                self.cover = True

    def spawn(self, window_width, window_height):
        raise NotImplementedError

    def update(self):
        self.lifebar.update()

class Player(mCharacter):
    def __init__(self, name, imagedict, window_width, window_height, cellsize, rendergroup):
        mCharacter.__init__(self, name, imagedict, 10.,window_width, window_height, cellsize, rendergroup)
        self.dead = False
        self.totalammo = 10.
        self.ammo = 10.        
        self.bulletsprite = bulletsprite.BulletSprite(self)
        rendergroup.add(self.bulletsprite)
        self.reloadCountdown = 0

    def spawn(self, window_width, window_height):
        return [random.randint(23,window_width-23),random.randint(32, window_height/2 - 32)]        

    def shoot(self, friendly_bullet_list, rendergroup):
        """shoots a bullet aiming the direction he is looking if there is ammo"""
        if self.ammo == 0 : return

        if self.direction == 1:
            bullet = objects.FriendlyBullet([self.rect.centerx - 1, self.rect.centery], [self.rect.centerx, self.rect.centery])
        elif self.direction == 2:
            bullet = objects.FriendlyBullet([self.rect.centerx + 1, self.rect.centery], [self.rect.centerx, self.rect.centery])
        elif self.direction == 3:
            bullet = objects.FriendlyBullet([self.rect.centerx, self.rect.centery - 1], [self.rect.centerx, self.rect.centery])
        elif self.direction == 4:
            bullet = objects.FriendlyBullet([self.rect.centerx, self.rect.centery + 1], [self.rect.centerx, self.rect.centery])

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
        mCharacter.update(self)
        if self.reloadCountdown == 1:
            self.reloadCountdown = 0
            self.ammo = 10.
        elif self.reloadCountdown > 1:
            self.reloadCountdown -= 1
        self.bulletsprite.update()