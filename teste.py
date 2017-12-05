import spritesheet
import pygame

In = 1

pygame.init()
w = 640
h = 480
size = (w,h)
screen = pygame.display.set_mode(size) 
c = pygame.time.Clock()

ss = spritesheet.spritesheet('Images/Walls.png')
teste = ss.image_at((121, 105, 30, 20))
#teste = ss.image_at((122, 146, 30, 30))

#ss = spritesheet.spritesheet('Images/ss-mercenaries.png')
# Sprite is 16x16 pixels at location 0,0 in the file...
"""baixo = ss.image_at((338, 182, 27, 34))

dr = ss.image_at((338, 142, 27, 34))

ur = ss.image_at((338, 60, 27, 34))

de = ss.image_at((338, 222, 27, 34))

ue = ss.image_at((258, 302, 27, 34))

direita = ss.image_at((340, 104, 27, 34))

esquerda = ss.image_at((336, 262, 27, 34))
cellsize = 5
cd = ss.image_at((90, 184, cellsize*5, cellsize*4))
cr = ss.image_at((90, 104, cellsize*5, cellsize*5))
cl = ss.image_at((90, 264, cellsize*5, cellsize*5))
cu = ss.image_at((91, 22, cellsize*5, cellsize*4))
lauxcdr = ss.image_at((206, 142, cellsize*5, cellsize*4))
rauxcdr = ss.image_at((206, 142, cellsize*5, cellsize*5))
lauxcdl = ss.image_at((214, 222, cellsize*5, cellsize*4))
rauxcdl = ss.image_at((214, 222, cellsize*5, cellsize*5))
lauxcur = ss.image_at((212, 62, cellsize*5, cellsize*4))
rauxcur = ss.image_at((212, 62, cellsize*5, cellsize*5))
lauxcul = ss.image_at((202, 304, cellsize*5, cellsize*4))
rauxcul = ss.image_at((202, 304, cellsize*5, cellsize*5))

d = [ss.image_at((8 + 40*i, 182, cellsize*6, cellsize*7)) for i in range(6)]
"""

image = teste

while True:
    screen.blit(image,(0,0))
    pygame.display.flip() # update the display
#images = []
# Load two images into an array, their transparent bit is (255, 255, 255)
#images = ss.images_at((0, 0, 16, 16),(17, 0, 16,16), colorkey=(255, 255, 255))