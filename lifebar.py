import pygame

black_color = (0, 0, 0)
green_color = (0, 255, 0)

class LifeBar(pygame.sprite.Sprite):
    """
    This class represents the bar that shows how many bullets the concerned character has loaded

    Parameters
    ----------
    owner : Character object (defined in characters.py)
        Specifies the character that will have this LifeBar

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
        self.owner = owner
        self.sizebar = self.owner.rect.width
        self.image = pygame.Surface((self.owner.rect.width,7))
        self.image.set_colorkey(black_color) # black transparent
        pygame.draw.rect(self.image, (0,255,0), (0,0,self.owner.rect.width,7),1)
        self.rect = self.image.get_rect()
        self.percent = 0
        
    def update(self):
        if self.percent != self.owner.hp/self.owner.totalhp:
            self.percent = self.owner.hp/self.owner.totalhp
            pygame.draw.rect(self.image, black_color, (1,1,self.sizebar-2,5))
            pygame.draw.rect(self.image, green_color, (1,1,int(self.sizebar * self.percent),5),0)
        self.rect.centerx = self.owner.rect.centerx
        self.rect.centery = self.owner.rect.centery - self.owner.rect.height/2 - 10
        
        if self.percent <= 0: #kill owner if hp == 0
            self.kill()
            if hasattr(self.owner, 'bulletsprite'): self.owner.bulletsprite.kill()
            self.owner.killhim()