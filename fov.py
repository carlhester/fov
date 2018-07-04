import pygame
import sys
import random

CELL = 10 
WIDTH = 600
HEIGHT = 600

pygame.init()
DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT))
cells = []

CELLS_WIDE = WIDTH / CELL
CELLS_TALL = HEIGHT / CELL

curr_x = 1 
curr_y = 1 
global rocks
rocks = [] 
for x in range(0, 130):
    x1 = random.randint(0, CELLS_WIDE)
    x2 = random.randint(0, CELLS_TALL)
    rocks.append((x1, x2))
#rocks = [(1,2), (1,3), (3, 3), (8, 6)]

#next_to_me = []
#for x in range(-1,CELLS_WIDE):
#    for y in range(-1, 2):
#        next_to_me.append((x, y))
border = []
for x in range(0, CELLS_WIDE):
    border.append((x, 0))
    border.append((x, CELLS_TALL))
for y in range(0, CELLS_TALL):
    border.append((0, y))
    border.append((CELLS_TALL, y))

for x in range(0, CELLS_WIDE):
    for y in range(0, CELLS_TALL):
        cells.append((x, y))

def get_line(start, end):
    global rocks
    #"""
    #Bresenham's Line Algorithm
    #Produces a list of tuples from start and end
 
    #>>> points1 = get_line((0, 0), (3, 4))
    #>>> points2 = get_line((3, 4), (0, 0))
    #>>> assert(set(points1) == set(points2))
    #>>> print points1
    #[(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    #>>> print points2
    #[(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    #"""
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points




while True:
    DISPLAY.fill(0)
    for x in range(0, CELLS_WIDE):
        pygame.draw.line(DISPLAY, (100, 100, 100), (x*CELL, 0), (x * CELL, WIDTH))
    for y in range(0, CELLS_TALL):
        pygame.draw.line(DISPLAY, (100, 100, 100), (0, y*CELL), (HEIGHT, y*CELL))

    for rock in rocks:
        pygame.draw.rect(DISPLAY, (0, 100, 100), (rock[0]*CELL, rock[1]*CELL, CELL, CELL))

    adjacent = []
    #for adj in next_to_me:
    #    adjacent.append((curr_x + adj[0], curr_y + adj[1]))

    #for adj_cell in adjacent:
    #    pygame.draw.rect(DISPLAY, (100, 0,0), (adj_cell[0] * CELL, adj_cell[1] * CELL, CELL, CELL))


    for edge in border:
        coords = get_line((curr_x, curr_y), edge)
        for sight in coords:
            if sight in rocks:
                break
            pygame.draw.rect(DISPLAY, (10, 100, 10), (sight[0]*CELL, sight[1]*CELL, CELL, CELL))

    pygame.draw.rect(DISPLAY, (100, 100, 100), (curr_x*CELL, curr_y*CELL, CELL, CELL))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            curr_y += 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            curr_y -= 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            curr_x += 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            curr_x -= 1

    pygame.display.update()
