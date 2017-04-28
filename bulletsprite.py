import pygame

#             R    G    B
Black     = (  0,   0,   0)
Green     = (  0, 255,   0)
Brown = (139, 69, 19)

class BulletSprite(pygame.sprite.Sprite):
    """shows a bar with the hitpoints the sprite"""
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self)
        self.sizebar = 20
        self.boss = boss
        self.image = pygame.Surface((self.sizebar,7))
        self.image.set_colorkey(Black) # black transparent
        pygame.draw.rect(self.image, Brown, (0,0,self.sizebar,7),1)
        self.rect = self.image.get_rect()
        self.oldpercent = 0
        
    def update(self):
        self.percent = self.boss.ammo / self.boss.totalammo
        if self.percent != self.oldpercent:
            pygame.draw.rect(self.image, Black, (1,1,self.sizebar-2,5)) # fill black
            pygame.draw.rect(self.image, Brown, (1,1,int(self.sizebar * self.percent),5),0) # fill green
        self.oldpercent = self.percent
        self.rect.centerx = self.boss.rect.centerx + self.boss.rect.width/2 + 12
        self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - 10