import random, pygame, math
from pygame.locals import *
import lifebar
import objects
import bulletsprite
import utils

class Character(pygame.sprite.Sprite):
    def __init__(self, name, imagedict, hp, screen, rendergroup, walls):
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
        self.walls = walls
        self.hp = hp
        self.totalhp = hp
        self.lifebar = lifebar.Lifebar(self)
        rendergroup.add(self.lifebar)
        self.cellsize = screen.cellsize
        self.walksize_x = self.cellsize*4
        self.walksize_y = self.cellsize*4
        self.screen = screen
        self.spawn()
        self.cover = False

    def checkwallcollision(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        return block_hit_list

    def checkcharactercollision(self):
        block_hit_list = []
        if hasattr(self, "other_characters"):
            block_hit_list = pygame.sprite.spritecollide(self, self.other_characters, False)
        return block_hit_list

    def fixPosition(self, hit_list, walking_direction):
        if hit_list:
            if walking_direction == 1:
                closest_one = hit_list[0].rect.right
            elif walking_direction == 2:
                closest_one = hit_list[0].rect.left
                closest_width = hit_list[0].rect.width
            elif walking_direction == 3:
                closest_one = hit_list[0].rect.bottom
            elif walking_direction == 4:
                closest_one = hit_list[0].rect.top              
            for hitted in hit_list:
                if walking_direction == 1 and hitted.rect.right > closest_one:
                    closest_one = hitted.rect.right
                elif walking_direction == 2 and hitted.rect.left < closest_one:
                    closest_one = hitted.rect.left
                elif walking_direction == 3 and hitted.rect.bottom > closest_one:
                    closest_one = hitted.rect.bottom
                elif walking_direction == 4 and hitted.rect.top < closest_one:
                    closest_one = hitted.rect.top
            previouswidth, previousheight = self.image.get_rect().width, self.image.get_rect().height
            if walking_direction == 1:
                self.x = closest_one
                self.image = self.imagedict['cr']
                self.rect = self.image.get_rect()
                if self.cover:
                    if self.blocked_direction == 3:
                        self.y += self.rect.height - previousheight
                    elif self.blocked_direction == 4:
                        self.y -= self.rect.height - previousheight
                [self.rect.x, self.rect.y] = [self.x, self.y]
            elif walking_direction == 2:
                self.x = closest_one
                self.image = self.imagedict['cl']
                self.rect = self.image.get_rect()
                self.x -= self.rect.width
                if self.cover:
                    if self.blocked_direction == 3:
                        self.y += self.rect.height - previousheight
                    elif self.blocked_direction == 4:
                        self.y -= self.rect.height - previousheight
                [self.rect.x, self.rect.y] = [self.x, self.y]
            elif walking_direction == 3:
                self.y = closest_one
                self.image = self.imagedict['cd']
                if self.cover:
                    if self.blocked_direction == 1:
                        self.x -= self.rect.width - previouswidth
                    if self.blocked_direction == 2:
                        self.x += self.rect.width - previouswidth
                self.rect = self.image.get_rect()
                [self.rect.x, self.rect.y] = [self.x, self.y]
            elif walking_direction == 4:
                self.y = closest_one
                self.image = self.imagedict['cu']
                self.rect = self.image.get_rect()
                self.y -= self.rect.height
                if self.cover:
                    if self.blocked_direction == 1:
                        self.x -= self.rect.width - previouswidth
                    if self.blocked_direction == 2:
                        self.x += self.rect.width - previouswidth
                [self.rect.x, self.rect.y] = [self.x, self.y]
            self.cover = True
            self.blocked_direction = walking_direction
        else:
            if self.cover:
                if self.blocked_direction in [1,2]:
                    if walking_direction in [3,4]:
                        return
                    else:
                        previousheight = self.image.get_rect().height
                        self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
                        self.rect = self.image.get_rect()
                        [self.rect.x, self.rect.y] = [self.x, self.y]
                        aux_hitted = self.checkwallcollision()+self.checkcharactercollision()
                        if aux_hitted:
                            self.y -= self.rect.height - previousheight
                            self.rect.y = self.y
                elif self.blocked_direction in [3,4]:
                    if walking_direction in [1, 2]:
                        return
            self.cover = False

    def updatePosition(self, eventkey):
        if eventkey in [K_a, K_d, K_w, K_s]:
            self.feetleft = not self.feetleft
            if eventkey == K_a:
                self.x -= self.walksize_x
                self.rect.x = self.x
                walking_direction = 1
            elif eventkey == K_d:
                self.x += self.walksize_x
                self.rect.x = self.x
                walking_direction = 2
            elif eventkey == K_w:
                self.y -= self.walksize_y
                self.rect.y = self.y
                walking_direction = 3
            elif eventkey == K_s:
                self.y += self.walksize_y
                self.rect.y = self.y
                walking_direction = 4
            if not self.cover:
                self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]
                self.rect = self.image.get_rect()
                [self.rect.x, self.rect.y] = [self.x, self.y]
        else:
            return
        self.fixPosition(self.checkwallcollision()+self.checkcharactercollision(), walking_direction)

    def findquadrant(self, angle):
        #this function finds in which region of the level the character is, rudl are equivalent to right, up, down and left
        pi = math.pi
        if angle > -pi/8 and angle <= pi/8:
            return "r"
        elif angle > pi/8 and angle <= 3*pi/8:
            return "ur"
        elif angle > 3*pi/8 and angle <= 5*pi/8:
            return "u"
        elif angle > 5*pi/8 and angle <= 7*pi/8:
            return "ul"
        elif angle <= -pi/8 and angle > -3*pi/8:
            return "dr"
        elif angle <= -3*pi/8 and angle > -5*pi/8:
            return "d"
        elif angle <= -5*pi/8 and angle > -7*pi/8:
            return "dl"
        else:
            return "l"

    def updatedirection(self):
        [x, y] = pygame.mouse.get_pos()
        distance = [x - self.x, y - self.y]
        angle = -math.atan2(distance[1], distance[0])
        newdirection = self.findquadrant(angle)
        self.currentdirection = newdirection
        self.image = self.imagedict[self.currentdirection][self.feettonum[self.feetleft]]

    def spawn(self):
        raise NotImplementedError

    def update(self):
        self.lifebar.update()

class Player(Character):
    def __init__(self, name, imagedict, screen, rendergroup, walls):
        Character.__init__(self, name, imagedict, 10., screen, rendergroup, walls)
        self.dead = False
        self.totalammo = 10.
        self.ammo = 10.        
        self.bulletsprite = bulletsprite.BulletSprite(self)
        rendergroup.add(self.bulletsprite)
        self.reloadCountdown = 0

    def spawn(self):
        new_spawn = [random.randrange(self.cellsize, self.screen.width-self.rect.width-self.cellsize, self.walksize_x),
        random.randrange(self.cellsize, self.screen.height/2, self.walksize_y)]
        [self.x, self.y] = new_spawn
        self.rect.x, self.rect.y = self.x, self.y
        while self.checkwallcollision():
            self.spawn()

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

class Player2(Character):
    def __init__(self, name, imagedict, screen, rendergroup, walls):
        Character.__init__(self, name, imagedict, 10., screen, rendergroup, walls)
        self.dead = False
        self.totalammo = 10.
        self.ammo = 10.        
        self.bulletsprite = bulletsprite.BulletSprite(self)
        rendergroup.add(self.bulletsprite)
        self.reloadCountdown = 0
        self.direction = 4

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
        else:
            return
        self.fixPosition(self.checkwallcollision()+self.checkcharactercollision(), self.direction)

    def spawn(self):
        new_spawn = [random.randrange(self.cellsize, self.screen.width-self.rect.width-self.cellsize, self.walksize_x),
        random.randrange(self.cellsize, self.screen.height/2, self.walksize_y)]
        [self.x, self.y] = new_spawn
        self.rect.x, self.rect.y = self.x, self.y
        while self.checkwallcollision():
            self.spawn()

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
        Character.update(self)
        if self.reloadCountdown == 1:
            self.reloadCountdown = 0
            self.ammo = 10.
        elif self.reloadCountdown > 1:
            self.reloadCountdown -= 1
        self.bulletsprite.update()


class Enemy(Character):
    count = 0

    def __init__(self, imagedict, player_list, screen, rendergroup, walls):
        Character.__init__(self, "enemy" + str(Enemy.count), imagedict, 5., screen, rendergroup, walls)
        Enemy.count += 1
        self.contbullet = 5
        self.auxbullet = 0
        self.player_list = player_list

    def spawn(self):
        new_spawn = [random.randrange(self.cellsize, self.screen.width-self.rect.width-self.cellsize, self.walksize_x),
        random.randrange(self.screen.height/2, self.screen.height - self.rect.height - self.cellsize, self.walksize_y)]
        [self.x, self.y] = new_spawn
        self.rect.x, self.rect.y = self.x, self.y
        while self.checkwallcollision():
            self.spawn()

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

    def updatedirection(self, player):
        distance = [player.x - self.x, player.y - self.y]
        angle = -math.atan2(distance[1], distance[0])
        newdirection = self.findquadrant(angle)
        self.image = self.imagedict[newdirection][self.feettonum[self.feetleft]]