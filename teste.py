import spritesheet
import pygame

In = 1

pygame.init()
w = 640
h = 480
size=(w,h)
screen = pygame.display.set_mode(size) 
c = pygame.time.Clock()

ss = spritesheet.spritesheet('ss-mercenaries.png')
# Sprite is 16x16 pixels at location 0,0 in the file...
#olhando pra cada direcao
baixo = ss.image_at((338, 182, 27, 34))
down = ss.image_at((92, 184, 23, 32))

direita = ss.image_at((340, 104, 27, 34))

esquerda = ss.image_at((336, 262, 27, 34))

cima = ss.image_at((338, 22, 27, 34))

dr = ss.image_at((90, 142, 23, 32))

de = ss.image_at((94, 222, 23, 32))

ur = ss.image_at((90, 62, 23, 32))

ue = ss.image_at((96, 304, 23, 32))


image = ur

while True:
    screen.blit(image,(0,0))
    pygame.display.flip() # update the display
#images = []
# Load two images into an array, their transparent bit is (255, 255, 255)
#images = ss.images_at((0, 0, 16, 16),(17, 0, 16,16), colorkey=(255, 255, 255))