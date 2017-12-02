import math, pygame

black_color = (0, 0, 0)
blue_color = (0, 0, 255)

class Bullet(pygame.sprite.Sprite):
    """
    This class represents the bullets shot in the game

    Parameters
    ----------
    target : Int List with length 2
        Specifies a point (x,y) that the Bullet should pass through

    origin : Int List with length 2        
        Specifies the point (x,y) that the Bullet should start from
    
    Atributes
    ---------
    image : Pygame's Sprite's image
        Represents the Bullet's image

    rect : Pygame's Sprite's rect
        Represents the Bullet's rectangle

    speed : Float
        Represents the speed in which the Bullet will move

    bullet_vector : Float List with length 2
        Represents the direction the Bullet should follow

    high : boolean
        True if the Bullet has passed through a low wall and False otherwise

    x : float
        Represents the x coordinate of the center of the object

    y : float
        Represents the y coordinate of the center of the object
    """
    def __init__(self, target, origin):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([2, 2])
        self.image.fill(black_color)
        self.rect = self.image.get_rect()
        self.rect.center = (origin[0], origin[1])
        self.x, self.y = float(self.rect.centerx), float(self.rect.centery)

        self.speed = 2.
        self.bullet_vector = self.find_bullet_vector(target)
        self.high = False

    def find_bullet_vector(self, target):
        distance = [target[0] - self.rect.centerx , target[1] - self.rect.centery]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0]/norm, distance[1]/norm]
        bullet_vector = [direction[0]*self.speed, direction[1] * self.speed]
        return bullet_vector

    def update(self, wall_list):
        """This method moves the bullet in the correct direction and checks for wall collision"""
        self.x += self.bullet_vector[0]
        self.y += self.bullet_vector[1]
        self.rect.center = (int(round(self.x)), int(round(self.y)))

        wall_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
        for wall in wall_hit_list:
            if wall.istall: 
                self.kill()
            else:
                self.high = True

class FriendlyBullet(Bullet):
    def update(self, enemy_list, wall_list):
        """This method calls the Bullet update method and checks for collision with enemies"""
        Bullet.update(self, wall_list)

        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in enemy_hit_list:
            if (not self.high) or (not enemy.movement.cover):
                self.kill()
                enemy.lifebar.hp -= 1

class EnemyBullet(Bullet):
    def update(self, player_list, wall_list):
        """This method calls the Bullet update method and checks for collision with players"""
        Bullet.update(self, wall_list)

        player_hit_list = pygame.sprite.spritecollide(self, player_list, False)
        for player in player_hit_list:
            if (not self.high) or (not player.movement.cover):
                self.kill()
                player.lifebar.hp -= 1

class Wall(pygame.sprite.Sprite):
    """
    This class represents the walls in the game

    Parameters
    ----------
    x : Int
        Specifies the x coordinate of the upper left point of the Wall

    y : Int
        Specifies the y coordinate of the upper left point of the Wall

    width : Int
        Specifies the width of the Wall

    height : Int
        Specifies the height of the Wall

    tallwall : boolean
        True if the Wall is tall and False otherwise

    Atributes
    ---------
    image : Pygame's Sprite's image
        Represents the Wall's image

    rect : Pygame's Sprite's rect
        Represents the Wall's rectangle

    istall : boolean
        True if the Wall is tall and False otherwise
    """
    def __init__(self, x, y, width, height, tallwall = True):
        pygame.sprite.Sprite.__init__(self)

        self.istall = tallwall
        self.image = pygame.Surface([width, height])
        self.image.fill(black_color) if self.istall else self.image.fill(blue_color)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x