import spritesheet
import pygame

In = 1

pygame.init()
w = 640
h = 480
size=(w,h)
screen = pygame.display.set_mode(size) 
c = pygame.time.Clock()

ss = spritesheet.spritesheet('Images/ss-mercenaries.png')
# Sprite is 16x16 pixels at location 0,0 in the file...
#olhando pra cada direcao
baixo = ss.image_at((338, 182, 27, 34))

dr = ss.image_at((338, 142, 27, 34))

ur = ss.image_at((338, 60, 27, 34))

de = ss.image_at((338, 222, 27, 34))

ue = ss.image_at((258, 302, 27, 34))

direita = ss.image_at((340, 104, 27, 34))

esquerda = ss.image_at((336, 262, 27, 34))
cellsize = 5
cd = ss.image_at((92, 182, cellsize*6, cellsize*6))

image = cd

while True:
    screen.blit(image,(0,0))
    pygame.display.flip() # update the display
#images = []
# Load two images into an array, their transparent bit is (255, 255, 255)
#images = ss.images_at((0, 0, 16, 16),(17, 0, 16,16), colorkey=(255, 255, 255))