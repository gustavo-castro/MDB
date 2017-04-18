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
image = ss.image_at((0, 0, 16, 16))
while True:
    screen.blit(image,(0,0))
    pygame.display.flip() # update the display
#images = []
# Load two images into an array, their transparent bit is (255, 255, 255)
#images = ss.images_at((0, 0, 16, 16),(17, 0, 16,16), colorkey=(255, 255, 255))