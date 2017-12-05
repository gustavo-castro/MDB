import pygame

import color


class LifeBar(pygame.sprite.Sprite):
    """
    This class represents the bar that shows how many hit points the concerned
    character has loaded

    Parameters
    ----------
    owner : Character object (defined in characters.py)
        Specifies the character that will have this LifeBar

    hp : Int
        Specifies the number of hitpoints the owner has

    Attributes
    ---------
    sizebar : Int
        Represents the size of the bar to be shown

    owner : Character object (defined in characters.py)
        Represents the character that will have this BulletBar

    image : Pygame's Sprite's image
        Represents the BulletBar's image

    rect : Pygame's Sprite's rect
        Represents the BulletBar's rectangle

    hp : Int
        Represents the current number of the owner's hitpoints

    total_hp : Int
        Represents the total number of the owner's hitpoints
    """
    def __init__(self, owner, hp):
        pygame.sprite.Sprite.__init__(self)
        self.owner = owner
        self.sizebar = self.owner.rect.width
        self.image = pygame.Surface((self.owner.rect.width, 7))
        self.image.set_colorkey(color.BLACK)
        pygame.draw.rect(
            self.image, color.GREEN, (0, 0, self.owner.rect.width, 7), 1)
        self.rect = self.image.get_rect()
        self.hp = hp
        self.total_hp = hp

    def update(self):
        hp_percent = self.hp/self.total_hp
        pygame.draw.rect(self.image, color.BLACK, (1, 1, self.sizebar-2, 5))
        pygame.draw.rect(self.image, color.GREEN, (1, 1, int(
            self.sizebar * hp_percent), 5), 0)
        self.rect.centerx = self.owner.rect.centerx
        self.rect.centery = self.owner.rect.centery - \
            self.owner.rect.height/2 - 10

        if hp_percent <= 0:  # kill owner if hp == 0
            self.kill()
            if hasattr(self.owner, 'bulletsprite'):
                self.owner.bulletsprite.kill()
            self.owner.killhim()
