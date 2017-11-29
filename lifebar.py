import pygame

#             R    G    B
Black     = (  0,   0,   0)
Green     = (  0, 255,   0)

class Lifebar(pygame.sprite.Sprite):
    """shows a bar with the hitpoints the sprite"""
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self)
        self.boss = boss
        self.image = pygame.Surface((self.boss.rect.width,7))
        self.image.set_colorkey(Black) # black transparent
        pygame.draw.rect(self.image, (0,255,0), (0,0,self.boss.rect.width,7),1)
        self.rect = self.image.get_rect()
        self.oldpercent = 0
        self.thewidth = self.boss.rect.width
        
    def update(self):
        self.percent = self.boss.hp / self.boss.totalhp
        if self.percent != self.oldpercent:
            pygame.draw.rect(self.image, Black, (1,1,self.thewidth-2,5)) # fill black
            pygame.draw.rect(self.image, Green, (1,1,int(self.thewidth * self.percent),5),0) # fill green
        self.oldpercent = self.percent
        self.rect.centerx = self.boss.rect.centerx
        self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - 10
        #kill boss if hp == 0
        if self.percent <= 0:
            self.kill()
            if hasattr(self.boss, 'bulletsprite'): self.boss.bulletsprite.kill()
            self.boss.killhim()