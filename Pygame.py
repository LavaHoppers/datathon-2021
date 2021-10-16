import random
import pygame, sys
import intersection
from pygame.locals  import *
import pandas
pygame.init()
DISPLAYSURF = pygame.display.set_mode((480, 480))
DISPLAYSURF.fill((255,255,255))
##FPS = pygame.time.Clock()
##FPS.tick(60)
test_pts = [(40, 40), (40, 440), (440, 440), (440, 40)]
test_edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

# for i in range(0, len(test_pts)-1):
#     x1=list[i][0]
#     y1=list[i][1]
#     x2=list[i+1][0]
#     y2=list[i+1][1]
#     pygame.draw.line(DISPLAYSURF,(0,0,0),(x1,y1),(x2,y2))
for edge in test_edges:
    pygame.draw.line(DISPLAYSURF,(0,0,0),test_pts[edge[0]],test_pts[edge[1]])

data = pandas.read_csv("2012-2020_Election_Data_with_2020_Wards.csv")
print(data.keys())

for x in range(480-1):
    for y in range(480-1):
        pygame.display.update()
        ot = (x, y)
        if intersection.contains(ot, test_pts, test_edges):
            DISPLAYSURF.set_at(ot, (0,0,255))
        else:
            DISPLAYSURF.set_at(ot, (255,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
   
    #FPS.tick(60)

    
