import random, pygame, math
from pygame.locals import *
import lifebar
import objects
import bulletsprite
import utils

class mCharacter(pygame.sprite.Sprite):
    """Character implementation using only the keyboard as input (instead of keyboard and mouse), will be used for multiplayer purposes"""
    def __init__(self, name, imagedict, hp, screen, rendergroup, walls):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.feetleft = True
        self.feettonum = {True : 2, False : 4}
        self.imagedict = imagedict
        self.image = self.imagedict['d'][2]
        self.rect = self.image.get_rect()
        self.walls = walls
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
        self.direction = 4
        self.cover = False

    def updatePosition(self, eventkey):
        if (eventkey == K_LEFT):
            self.x -= self.walksize_x
            self.rect.x = self.x
            self.image = self.imagedict['l'][self.feettonum[self.feetleft]]
            self.direction = 1
            self.cover = False
        elif (eventkey == K_RIGHT):
            self.x += self.walksize_x
            self.rect.x = self.x
            self.image = self.imagedict['r'][self.feettonum[self.feetleft]]
            self.direction = 2
            self.cover = False
        elif (eventkey == K_UP):
            self.y -= self.walksize_y
            self.rect.y = self.y
            self.image = self.imagedict['u'][self.feettonum[self.feetleft]]
            self.direction = 3
            self.cover = False
        elif (eventkey == K_DOWN):
            self.y += self.walksize_y
            self.rect.y = self.y
            self.image = self.imagedict['d'][self.feettonum[self.feetleft]]
            self.direction = 4
            self.cover = False
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        if block_hit_list:
            if self.direction == 1:
                self.x += self.walksize_x
                self.rect.x = self.x
                self.cover = True
            elif self.direction == 2:
                self.x -= self.walksize_x
                self.rect.x = self.x
                self.cover = True
            elif self.direction == 3:
                self.y += self.walksize_y
                self.rect.y = self.y
                self.cover = True
            elif self.direction == 4:
                self.y -= self.walksize_y
                self.rect.y = self.y
                self.cover = True

    def spawn(self):
        raise NotImplementedError

    def update(self):
        self.lifebar.update()

class Player(mCharacter):
    def __init__(self, name, imagedict, screen, rendergroup, walls):
        mCharacter.__init__(self, name, imagedict, 10., screen, rendergroup, walls)
        self.dead = False
        self.totalammo = 10.
        self.ammo = 10.        
        self.bulletsprite = bulletsprite.BulletSprite(self)
        rendergroup.add(self.bulletsprite)
        self.reloadCountdown = 0

    def spawn(self):
        return [random.randrange(self.cellsize, self.screen.width, self.walksize_x), random.randrange(self.cellsize, self.screen.height/2, self.walksize_y)]



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