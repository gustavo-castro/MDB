import pygame
import color


class BulletBar(pygame.sprite.Sprite):
    """
    This class represents the bar that shows how many bullets the
    concerned character has loaded

    Parameters
    ----------
    owner : Character object (defined in characters.py)
        Specifies the character that will have this BulletBar

    ammo : Float
        Specifies how many bullets the owner can carry

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

    ammo : Float
        Specifies how many bullets the owner has at the moment

    total_ammo : Float
        Specifies how many bullets the owner can carry
    """
    def __init__(self, owner, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.sizebar = 20
        self.owner = owner
        self.image = pygame.Surface((self.sizebar, 7))
        self.image.set_colorkey(color.BLACK)
        pygame.draw.rect(self.image, color.BROWN, (0, 0, self.sizebar, 7), 1)
        self.rect = self.image.get_rect()
        self.ammo = ammo
        self.total_ammo = ammo

    def update(self):
        bullet_percent = self.ammo/self.total_ammo
        pygame.draw.rect(self.image, color.BLACK, (1, 1, self.sizebar-2, 5))
        pygame.draw.rect(self.image, color.BROWN, (1, 1, int(
            self.sizebar*bullet_percent), 5), 0)
        self.rect.centerx = self.owner.rect.centerx + \
            self.owner.rect.width/2 + 12
        self.rect.centery = self.owner.rect.centery - \
            self.owner.rect.height/2 - 10
