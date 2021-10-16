import pygame, sys
from pygame.locals  import *
pygame.init()
DISPLAYSURF = pygame.display.set_mode((300,300))
DISPLAYSURF.fill((255,255,255))
FPS = pygame.time.Clock()
FPS.tick(60)
list=[(1,1),(3,5),(7,9)]
for i in range(0, len(list)-1):
    x1=list[i][0]
    y1=list[i][1]
    x2=list[i+1][0]
    y2=list[i+1][1]
    pygame.draw.line(DISPLAYSURF,(0,0,0),(x1,y1),(x2,y2))
while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
   
    FPS.tick(60)

    
