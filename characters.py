import random
import pygame
import pygame.locals
import math

import lifebar
import objects
import bulletsprite

player1_keys = [pygame.locals.K_a, pygame.locals.K_d,
                pygame.locals.K_w, pygame.locals.K_s]


class Movement(object):
    """
    This class represents the movement aspects of the concerned character

    Parameters
    ----------
    screen : Screen object (as defined in utils.py)
        Specifies the screen attributes of the game

    walls : Wall object (as defined in objects.py)
        Specifies the walls present in the game

    Attributes
    ---------
    feet_left : boolean
        True if the character is walking on his left foot and False otherwise

    current_direction : string
        Represents the character's current direction (the one he is looking to)

    screen : Screen object
        Represents the screen attributes of the game

    step_size_x, step_size_y : Int
        Represent the size of the character's step in the x and y axis

    walls : Wall object
        Represents the walls present in the game

    shot : Int
        Positive if the character has shot recently and 0 otherwise

    cover : boolean
        True if the character is in cover (against a wall) and False otherwise
    """
    def __init__(self, screen, walls):
        self.feet_left = True
        self.current_direction = 'd'
        self.screen = screen
        self.step_size_x = self.screen.cellsize*4
        self.step_size_y = self.screen.cellsize*4
        self.walls = walls
        self.shot = 0
        self.cover = False

    def which_leg(self):
        if self.feet_left:
            return "left"
        else:
            return "right"


class Character(pygame.sprite.Sprite):
    """
    This class represents the characters of the game

    Parameters
    ----------
    name : string
        Specifies the character's name

    imagedict : dictionary
        Represents all the images that will represent the character in the
        form of a dictionary

    hp : Int
        Specifies the number of hit points the character will have

    screen : Screen object (as defined in utils.py)
        Specifies the screen attributes of the game

    rendergroup : Pygame's Sprite's Group
        Specifies the group that will be rendered to the display of the game

    walls : Wall object (as defined in objects.py)
        Specifies the walls present in the game

    Attributes
    ---------
    name : string
        Represents the character's name

    movement : Movement object
        Represents the character's movement characteristics

    imagedict : dictionary
        Represents all the images that will represent the character in the
        form of a dictionary

    image : Pygame's Sprite's image
        Represents the character's image

    rect : Pygame's Sprite's rect
        Represents the character's rectangle

    walls : Wall object
        Represents the walls present in the game
    """
    def __init__(self, name, imagedict, hp, screen, rendergroup, walls,
                 player_list, enemy_list):
        pygame.sprite.Sprite.__init__(self)

        self.player_list = player_list
        self.enemy_list = enemy_list
        self.name = name
        self.movement = Movement(screen, walls)
        self.imagedict = imagedict
        self.image = self.imagedict[self.movement.current_direction][
            self.movement.which_leg()]
        self.rect = self.image.get_rect()
        self.lifebar = lifebar.LifeBar(self, hp)
        rendergroup.add(self, self.lifebar)
        self.spawn()
        self.moved = False
        self.dead = False

    def check_wall_collision(self):
        block_hit_list = pygame.sprite.spritecollide(
            self, self.movement.walls, False)
        return block_hit_list

    def check_character_collision(self):
        aux = self.enemy_list.copy()
        aux.add(self.player_list)
        aux.remove(self)
        return pygame.sprite.spritecollide(self, aux, False)

    def fix_position(self, hit_list, walking_direction):
        if hit_list:
            if walking_direction == 1:
                closest_one = hit_list[0].rect.right
            elif walking_direction == 2:
                closest_one = hit_list[0].rect.left
            elif walking_direction == 3:
                closest_one = hit_list[0].rect.bottom
            elif walking_direction == 4:
                closest_one = hit_list[0].rect.top
            for hitted in hit_list:
                if walking_direction == 1 and hitted.rect.right > closest_one:
                    closest_one = hitted.rect.right
                elif walking_direction == 2 and hitted.rect.left < closest_one:
                    closest_one = hitted.rect.left
                elif walking_direction == 3 and hitted.rect.bottom > \
                        closest_one:
                    closest_one = hitted.rect.bottom
                elif walking_direction == 4 and hitted.rect.top < closest_one:
                    closest_one = hitted.rect.top
            previous_width = self.image.get_rect().width
            previous_height = self.image.get_rect().height
            if walking_direction == 1:
                self.x = closest_one
                self.cover_direction = "cr"
                self.image = self.imagedict[self.cover_direction]["cover"]
                self.rect = self.image.get_rect()
                if self.movement.cover:
                    if self.blocked_direction == 3:
                        self.y += self.rect.height - previous_height
                    elif self.blocked_direction == 4:
                        self.y -= self.rect.height - previous_height
                [self.rect.x, self.rect.y] = [self.x, self.y]
            elif walking_direction == 2:
                self.x = closest_one
                self.cover_direction = "cl"
                self.image = self.imagedict[self.cover_direction]["cover"]
                self.rect = self.image.get_rect()
                self.x -= self.rect.width
                if self.movement.cover:
                    if self.blocked_direction == 3:
                        self.y += self.rect.height - previous_height
                    elif self.blocked_direction == 4:
                        self.y -= self.rect.height - previous_height
                [self.rect.x, self.rect.y] = [self.x, self.y]
            elif walking_direction == 3:
                self.y = closest_one
                self.cover_direction = "cd"
                self.image = self.imagedict[self.cover_direction]["cover"]
                if self.movement.cover:
                    if self.blocked_direction == 1:
                        self.x -= self.rect.width - previous_width
                    if self.blocked_direction == 2:
                        self.x += self.rect.width - previous_width
                self.rect = self.image.get_rect()
                [self.rect.x, self.rect.y] = [self.x, self.y]
            elif walking_direction == 4:
                self.y = closest_one
                self.cover_direction = "cu"
                self.image = self.imagedict[self.cover_direction]["cover"]
                self.rect = self.image.get_rect()
                self.y -= self.rect.height
                if self.movement.cover:
                    if self.blocked_direction == 1:
                        self.x -= self.rect.width - previous_width
                    if self.blocked_direction == 2:
                        self.x += self.rect.width - previous_width
                [self.rect.x, self.rect.y] = [self.x, self.y]
            self.movement.cover = True
            self.blocked_direction = walking_direction
        else:
            if self.movement.cover or (self.movement.shot and self.wasincover):
                if self.blocked_direction in [1, 2]:
                    if walking_direction in [3, 4]:
                        self.movement.cover = True
                        self.moved = False
                        return
                    else:
                        previous_height = self.image.get_rect().height
                        self.image = self.imagedict[
                            self.movement.current_direction][
                                self.movement.which_leg()]
                        self.rect = self.image.get_rect()
                        [self.rect.x, self.rect.y] = [self.x, self.y]
                        aux_hitted = self.check_wall_collision() + \
                            self.check_character_collision()
                        if aux_hitted:
                            self.y -= self.rect.height - previous_height
                            self.rect.y = self.y
                elif self.blocked_direction in [3, 4]:
                    if walking_direction in [1, 2]:
                        self.movement.cover = True
                        self.moved = False
                        return
                    else:
                        previous_width = self.image.get_rect().width
                        self.image = self.imagedict[
                            self.movement.current_direction][
                                self.movement.which_leg()]
                        self.rect = self.image.get_rect()
                        [self.rect.x, self.rect.y] = [self.x, self.y]
                        aux_hitted = self.check_wall_collision() + \
                            self.check_character_collision()
                        if aux_hitted:
                            self.x -= self.rect.width - previous_width
                            self.rect.x = self.x
            self.movement.cover = False

    def update_position(self, eventkey):
        if eventkey in player1_keys:
            self.movement.feet_left = not self.movement.feet_left
            if eventkey == pygame.locals.K_a:
                self.x -= self.movement.step_size_x
                self.rect.x = self.x
                walking_direction = 1
            elif eventkey == pygame.locals.K_d:
                self.x += self.movement.step_size_x
                self.rect.x = self.x
                walking_direction = 2
            elif eventkey == pygame.locals.K_w:
                self.y -= self.movement.step_size_y
                self.rect.y = self.y
                walking_direction = 3
            elif eventkey == pygame.locals.K_s:
                self.y += self.movement.step_size_y
                self.rect.y = self.y
                walking_direction = 4
            if not self.movement.cover and not (
                    self.movement.shot and self.wasincover):
                self.image = self.imagedict[self.movement.current_direction][
                    self.movement.which_leg()]
                self.rect = self.image.get_rect()
                [self.rect.x, self.rect.y] = [self.x, self.y]
            self.moved = True
        else:
            return
        self.fix_position(self.check_wall_collision() +
                          self.check_character_collision(), walking_direction)

    @staticmethod
    def find_quadrant(angle):
        """
        Finds in which region of the level the character is,
        rudl are equivalent to right, up, down and left
        :param angle: float
        :return: string
        """
        pi = math.pi
        if -pi/8 < angle <= pi/8:
            return "r"
        elif pi/8 < angle <= 3*pi/8:
            return "ur"
        elif 3*pi/8 < angle <= 5*pi/8:
            return "u"
        elif 5*pi/8 < angle <= 7*pi/8:
            return "ul"
        elif -3*pi/8 < angle <= -pi/8:
            return "dr"
        elif -5*pi/8 < angle <= -3*pi/8:
            return "d"
        elif -7*pi/8 < angle <= -5*pi/8:
            return "dl"
        else:
            return "l"

    def update_direction(self):
        [x, y] = pygame.mouse.get_pos()
        distance = [x - self.x, y - self.y]
        angle = -math.atan2(distance[1], distance[0])
        newdirection = self.find_quadrant(angle)
        self.movement.current_direction = newdirection
        self.image = self.imagedict[
            self.movement.current_direction][
                self.movement.which_leg()]

    def spawn(self):
        self.x = random.randrange(self.movement.screen.cellsize,
                                  self.movement.screen.width - self.rect.width
                                  - self.movement.screen.cellsize,
                                  self.movement.step_size_x,)
        self.y = random.randrange(self.movement.screen.cellsize,
                                  self.movement.screen.height/2,
                                  self.movement.step_size_y)
        self.rect.x, self.rect.y = self.x, self.y
        while self.check_wall_collision()+self.check_character_collision():
            self.spawn()

    def reload(self):
        self.reloadCountdown = 10

    def killhim(self):
        self.dead = True
        self.kill()

    def update(self):
        self.lifebar.update()


class Player(Character):
    def __init__(self, name, imagedict, screen, rendergroup, walls,
                 player_list, enemy_list):
        Character.__init__(self, name, imagedict, 10., screen,
                           rendergroup, walls, player_list, enemy_list)
        player_list.add(self)
        self.dead = False
        self.bulletsprite = bulletsprite.BulletBar(self, 10.)
        rendergroup.add(self.bulletsprite)
        self.reloadCountdown = 0

    def shoot(self, friendly_bullet_list, rendergroup):
        """shoots a bullet where the mouse is pointed if there is ammo"""
        if self.bulletsprite.ammo == 0:
            return

        bullet = objects.FriendlyBullet(pygame.mouse.get_pos(), [
            self.rect.centerx, self.rect.centery])

        bullet.add(friendly_bullet_list, rendergroup)
        if not self.movement.shot:
            self.lastimage = self.image
            if self.movement.cover:
                [x, y] = pygame.mouse.get_pos()
                distance = [x - self.x, y - self.y]
                angle = -math.atan2(distance[1], distance[0])
                shoot_direction = self.find_quadrant(angle)
                if shoot_direction in ["r", "u", "l", "d"]:
                    self.image = self.imagedict["c"+shoot_direction]["shoot"]
                else:
                    if self.blocked_direction in ["r", "l"]:
                        self.image = self.imagedict["c"+shoot_direction][
                            "left"]
                    else:
                        self.image = self.imagedict["c"+shoot_direction][
                            "right"]
            else:
                self.image = self.imagedict[self.movement.current_direction][
                    "shoot"]
            self.rect = self.image.get_rect()
            [self.rect.x, self.rect.y] = [self.x, self.y]

        if not self.movement.shot:
            self.wasincover = self.movement.cover
        self.movement.cover = False
        self.moved = False

        self.movement.shot = 1
        self.bulletsprite.ammo -= 1

    def stopshoot(self):
        self.movement.shot = 0
        if not self.moved:
            self.image = self.lastimage
            if self.wasincover:
                self.movement.cover = True

    def update(self):
        Character.update(self)
        if self.reloadCountdown == 1:
            self.reloadCountdown = 0
            self.bulletsprite.ammo = 10.
        elif self.reloadCountdown > 1:
            self.reloadCountdown -= 1
        self.bulletsprite.update()

        if not self.movement.cover and not self.movement.shot:
            self.update_direction()

        if self.movement.shot > 4:
            self.stopshoot()
        elif self.movement.shot > 0:
            self.movement.shot += 1


class Player2(Character):
    def __init__(self, name, imagedict, screen, rendergroup, walls,
                 player_list, enemy_list, is_multi_mode):
        Character.__init__(self, name, imagedict, 10., screen,
                           rendergroup, walls, player_list, enemy_list)
        if is_multi_mode:
            enemy_list.add(self)
        else:
            player_list.add(self)
        self.dead = False
        self.bulletsprite = bulletsprite.BulletBar(self, 10.)
        rendergroup.add(self.bulletsprite)
        self.reloadCountdown = 0
        self.direction = 4

    def update_position(self, eventkey):
        if (eventkey == pygame.locals.K_LEFT):
            self.x -= self.movement.step_size_x
            self.rect.x = self.x
            self.image = self.imagedict['l'][self.movement.which_leg()]
            self.direction = 1
            self.movement.cover = False
        elif (eventkey == pygame.locals.K_RIGHT):
            self.x += self.movement.step_size_x
            self.rect.x = self.x
            self.image = self.imagedict['r'][self.movement.which_leg()]
            self.direction = 2
            self.movement.cover = False
        elif (eventkey == pygame.locals.K_UP):
            self.y -= self.movement.step_size_y
            self.rect.y = self.y
            self.image = self.imagedict['u'][self.movement.which_leg()]
            self.direction = 3
            self.movement.cover = False
        elif (eventkey == pygame.locals.K_DOWN):
            self.y += self.movement.step_size_y
            self.rect.y = self.y
            self.image = self.imagedict['d'][self.movement.which_leg()]
            self.direction = 4
            self.movement.cover = False
        else:
            return
        self.fix_position(self.check_wall_collision() +
                          self.check_character_collision(), self.direction)

    def shoot(self, friendly_bullet_list, rendergroup):
        """
        shoots a bullet aiming the direction he is looking if there is ammo
        """
        if self.bulletsprite.ammo == 0:
            return

        if self.direction == 1:
            bullet = objects.FriendlyBullet([
                self.rect.centerx - 1, self.rect.centery], [
                self.rect.centerx, self.rect.centery])
        elif self.direction == 2:
            bullet = objects.FriendlyBullet([
                self.rect.centerx + 1, self.rect.centery], [
                self.rect.centerx, self.rect.centery])
        elif self.direction == 3:
            bullet = objects.FriendlyBullet([
                self.rect.centerx, self.rect.centery - 1], [
                self.rect.centerx, self.rect.centery])
        elif self.direction == 4:
            bullet = objects.FriendlyBullet([
                self.rect.centerx, self.rect.centery + 1], [
                self.rect.centerx, self.rect.centery])

        bullet.add(friendly_bullet_list, rendergroup)

        self.bulletsprite.ammo -= 1

    def update(self):
        Character.update(self)
        if self.reloadCountdown == 1:
            self.reloadCountdown = 0
            self.bulletsprite.ammo = 10.
        elif self.reloadCountdown > 1:
            self.reloadCountdown -= 1
        self.bulletsprite.update()


class Enemy(Character):
    count = 0

    def __init__(self, imagedict, player_list, screen, rendergroup, walls,
                 enemy_list):
        Character.__init__(self, "enemy" + str(Enemy.count),
                           imagedict, 5., screen, rendergroup, walls,
                           player_list, enemy_list)
        Enemy.count += 1
        self.contbullet = 5
        self.bullettimer = 0
        self.player_list = player_list
        self.bulletsprite = bulletsprite.BulletBar(self, 5.)
        rendergroup.add(self.bulletsprite)
        self.reloadCountdown = 0
        enemy_list.add(self)

    def spawn(self):
        self.x = random.randrange(self.movement.screen.cellsize,
                                  self.movement.screen.width - self.rect.width
                                  - self.movement.screen.cellsize,
                                  self.movement.step_size_x)
        self.y = random.randrange(self.movement.screen.height/2,
                                  self.movement.screen.height
                                  - self.rect.height -
                                  self.movement.screen.cellsize,
                                  self.movement.step_size_y)
        self.rect.x, self.rect.y = self.x, self.y
        while self.check_wall_collision()+self.check_character_collision():
            self.spawn()

    def shoot(self, enemy_bullet_list, rendergroup):
        """shoots a bullet at the player"""
        if self.bulletsprite.ammo == 0:
            if self.reloadCountdown == 0:
                self.reload()
                self.image = self.imagedict[self.movement.current_direction][
                    self.movement.which_leg()]
            return

        dist = float('inf')
        if self.player_list:
            for player in self.player_list.sprites():
                tempdist = (player.rect.centerx - self.rect.centerx)**2 + (
                    player.rect.centery - self.rect.centery)**2
                if tempdist < dist:
                    dist = tempdist
                    closestplayer = player
            self.update_direction(closestplayer)
            bullet = objects.EnemyBullet([
                closestplayer.rect.centerx, closestplayer.rect.centery], [
                self.rect.centerx, self.rect.centery])
            bullet.add(enemy_bullet_list, rendergroup)

        self.image = self.imagedict[self.movement.current_direction]["shoot"]

        self.bulletsprite.ammo -= 1

    def update(self, enemy_bullet_list, rendergroup):
        Character.update(self)
        if self.bullettimer == self.contbullet:
            self.shoot(enemy_bullet_list, rendergroup)
            self.bullettimer = 0
        self.bullettimer += 1

        if self.reloadCountdown == 1:
            self.reloadCountdown = 0
            self.bulletsprite.ammo = 10.
        elif self.reloadCountdown > 1:
            self.reloadCountdown -= 1
        self.bulletsprite.update()

    def update_direction(self, player):
        distance = [player.x - self.x, player.y - self.y]
        angle = -math.atan2(distance[1], distance[0])
        newdirection = self.find_quadrant(angle)
        self.movement.current_direction = newdirection
        self.image = self.imagedict[newdirection][
            self.movement.which_leg()]
