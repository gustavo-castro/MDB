import math, pygame

#             R    G    B
black     = (  0,   0,   0)
blue      = (  0,   0, 255)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, target, origin):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([2, 2])
        self.image.fill(black)

        self.target = target

        self.rect = self.image.get_rect()

        self.rect.center = (origin[0], origin[1])

        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.speed = 2.

        self.bullet_vector = self.findbv()


    def findbv(self):
        distance = [self.target[0] - self.rect.centerx , self.target[1] - self.rect.centery]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1 ] / norm]
        bullet_vector = [direction[0] * self.speed, direction[1] * self.speed]
        return bullet_vector

    def update(self, wall_list):
        self.x += self.bullet_vector[0]
        self.y += self.bullet_vector[1]

        self.rect.center = (int(round(self.x)), int(round(self.y)))

        wall_hit_list = pygame.sprite.spritecollide(self, wall_list, False)

        for wall in wall_hit_list:
            self.kill()

class FriendlyBullet(Bullet):
    def update(self, enemy_list, wall_list):
        """moves bullet then checks if it hit an enemy"""
        Bullet.update(self, wall_list)

        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)

        for enemy in enemy_hit_list:
            self.kill()
            enemy.hp -= 1

class EnemyBullet(Bullet):
    def update(self, player_list, wall_list):
        """moves bullet then checks if it hit a player"""
        Bullet.update(self, wall_list)

        player_hit_list = pygame.sprite.spritecollide(self, player_list, False)

        for player in player_hit_list:
            self.kill()
            player.hp -= 1

class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into"""
    def __init__(self, x, y, width, height):
        """ Constructor for the wall"""
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(black)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x