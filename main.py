import sys
import time
import pygame
from pygame.locals import QUIT
import numpy as np
from random import randint
from functools import reduce

pi = np.pi
cos = np.cos
sin = np.sin

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hello World!')

# define cube points
cube_points = np.array([
    [0, 1, 1],
    [0, 0, 1],
    [0, 0, 0],
    [0, 1, 0],
    [1, 1, 1],
    [1, 0, 1],
    [1, 0, 0],
    [1, 1, 0]
])

# project to 2d
projection_2d = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])

cube_indices = np.array([
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7]
])    

#enlarge cube
enlarge = np.array([
    [50,  0,  0],
    [ 0, 50,  0],
    [ 0,  0, 50]
])

# translation vector 
translation = np.array([
[150, 200, 0]
])

def create_xrotation_matrix(rad_angle):
  return np.array([
    [1,              0,               0],
    [0, cos(rad_angle), -sin(rad_angle)],
    [0, sin(rad_angle),  cos(rad_angle)]
  ])

def create_yrotation_matrix(rad_angle):
  return np.array([
    [cos(rad_angle),  0, sin(rad_angle)],
    [0,               1,              0],
    [-sin(rad_angle), 0, cos(rad_angle)]
  ])
  
def create_zrotation_matrix(rad_angle):
  return np.array([
    [cos(rad_angle), -sin(rad_angle), 0],
    [sin(rad_angle),  cos(rad_angle), 0],
    [             0,               0, 1]
  ])

def z_scaling(points):
  avg = 0
  for point in points:
    avg += point[2]
  avg /= len(points)
  avg = 100 / (avg + 0000.1)
  return np.array([
      [avg,  0,  0],
      [ 0, avg,  0],
      [ 0,  0, avg]
  ])

cube_points = cube_points@enlarge
cube_points += translation
print(cube_points)

origin = np.array([175, 225, 25])

# physics
points_2d = cube_points

# rotation matrices
x_rotation_matrix = create_xrotation_matrix(pi/100)
y_rotation_matrix = create_yrotation_matrix(pi/100)
z_rotation_matrix = create_zrotation_matrix(pi/100)

movement_vector = np.array([randint(-2, 2), randint(-2, 2), 0])

right_collision = False
left_collision = False
bottom_collision = False
top_collision = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()

    points_2d += movement_vector
    origin += movement_vector

    for point in points_2d:
      if point[0] >= SCREEN_WIDTH and not right_collision:
        right_collision = True
        left_collision = False
        movement_vector[0] *= -1
      elif point[0] <= 0 and not left_collision:
        left_collision = True
        right_collision = False
        movement_vector[0] *= -1
      if point[1] >= SCREEN_HEIGHT and not bottom_collision:
        bottom_collision = True
        top_collsion = False
        movement_vector[1] *= -1
      elif point[1] <= 0 and not top_collision:
        top_collision = True
        bottom_collision = False
        movement_vector[1] *= -1
  
    points_2d -= origin
    '''
    # scale cube based on z value
    print('========')
    print(z_scaling(points_2d))
    z_scale = z_scaling(points_2d)
    points_2d = points_2d@z_scale
    '''
  
    # rotate cube
    points_2d = points_2d@x_rotation_matrix
    points_2d = points_2d@y_rotation_matrix
    points_2d = points_2d@z_rotation_matrix

    points_2d += origin

    # redraw bg
    DISPLAYSURF.fill((0, 0, 0))
  
    for idx in cube_indices:
      pygame.draw.line(DISPLAYSURF, (255, 0, 0), (points_2d[idx[0]][0], points_2d[idx[0]][1]), (points_2d[idx[1]][0], points_2d[idx[1]][1]))

    time.sleep(.1)
      
    pygame.display.update()
