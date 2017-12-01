import pygame

black_color = (0, 0, 0)
brown_color = (139, 69, 19)

class BulletBar(pygame.sprite.Sprite):
    """
    This class represents the bar that shows how many bullets the concerned character has loaded

    Parameters
    ----------
    owner : Character object (defined in characters.py)
        Specifies the character that will have this BulletBar

    Atributes
    ---------
    sizebar : Int
        Represents the size of the bar to be shown

    owner : Character object (defined in characters.py)
        Represents the character that will have this BulletBar

    image : Pygame's Sprite's image
        Represents the BulletBar's image

    rect : Pygame's Sprite's rect
        Represents the BulletBar's rectangle

    percent : Float
        Represents the percentage of bullets that the BulletBar's owner has
    """
    def __init__(self, owner):
        pygame.sprite.Sprite.__init__(self)
        self.sizebar = 20
        self.owner = owner
        self.image = pygame.Surface((self.sizebar,7))
        self.image.set_colorkey(black_color) # black transparent
        pygame.draw.rect(self.image, brown_color, (0, 0, self.sizebar,7), 1)
        self.rect = self.image.get_rect()
        self.percent = 0.
        
    def update(self):
        if self.percent != self.owner.ammo/self.owner.totalammo:
            self.percent = self.owner.ammo / self.owner.totalammo
            pygame.draw.rect(self.image, black_color, (1, 1, self.sizebar-2, 5)) # fill black
            pygame.draw.rect(self.image, brown_color, (1, 1, int(self.sizebar*self.percent), 5), 0) # fill green
        self.rect.centerx = self.owner.rect.centerx + self.owner.rect.width/2 + 12
        self.rect.centery = self.owner.rect.centery - self.owner.rect.height/2 - 10