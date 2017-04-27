import math, pygame

#             R    G    B
black     = (  0,   0,   0)
blue      = (  0,   0, 255)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, target, shooter):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([2, 2])
        self.image.fill(black)

        self.shooter_x = shooter[0]
        self.shooter_y = shooter[1]
        self.target_x = target[0]
        self.target_y = target[1]

        self.x = float(self.shooter_x)
        self.y = float(self.shooter_y)

        self.speed = 20.

        self.bullet_vector = self.findbv()

        self.rect = self.image.get_rect()

    def findbv(self):
        distance = [self.target_x - self.shooter_x , self.target_y - self.shooter_y]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1 ] / norm]
        bullet_vector = [direction[0] * self.speed, direction[1] * self.speed]
        return bullet_vector

    def update(self):
        self.x += self.bullet_vector[0]
        self.y += self.bullet_vector[1]

        self.rect.centerx = int(round(self.x))
        self.rect.centery = int(round(self.y))

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