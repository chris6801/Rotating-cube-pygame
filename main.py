import sys
import time
import pygame
from pygame.locals import QUIT
import numpy as np
from random import randint

pi = np.pi
cos = np.cos
sin = np.sin

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

MIN_Z = 101
MAX_Z = 1000

pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hello World!')

# define cube points
cube_points = np.array([
    [0, 1, 1, 1],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [0, 1, 0, 1],
    [1, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 0, 1]
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
    [50,  0,  0, 0],
    [ 0, 50,  0, 0],
    [ 0,  0, 50, 0],
    [ 0,  0,  0, 1]
])

# translation and inverse translation 
translation_matrix = np.array([
    [1, 0, 0, 150],
    [0, 1, 0, 200],
    [0, 0, 1,   0],
    [0, 0, 0,   1]
])

inverse_translation_matrix = np.array([
    [1, 0, 0, -150],
    [0, 1, 0, -200],
    [0, 0, 1,    0],
    [0, 0, 0,    1]
])

def create_xrotation_matrix(rad_angle):
  return np.array([
    [1,              0,               0, 0],
    [0, cos(rad_angle), -sin(rad_angle), 0],
    [0, sin(rad_angle),  cos(rad_angle), 0],
    [0,              0,               0, 1]
  ])

def create_yrotation_matrix(rad_angle):
  return np.array([
    [cos(rad_angle),  0, sin(rad_angle), 0],
    [             0,  1,              0, 0],
    [-sin(rad_angle), 0, cos(rad_angle), 0],
    [             0,  0,              0, 1]
  ])
  
def create_zrotation_matrix(rad_angle):
  return np.array([
    [cos(rad_angle), -sin(rad_angle), 0, 0],
    [sin(rad_angle),  cos(rad_angle), 0, 0],
    [             0,               0, 1, 0],
    [             0,               0, 0, 1]
  ])

def find_origin(points):
  return np.array([
    points[6][0] - ((points[6][0] - points[0][0]) //2),
    points[6][1] - ((points[6][1] - points[0][1]) //2),
    points[6][2] - ((points[6][2] - points[0][2]) //2),
                                                    0
  ])

def create_perspective_projection_matrix(fov, aspect_ratio, near, far):
  fov_rad = fov * pi / 180
  f = 1 / np.tan(fov_rad / 2)
  return np.array([
    [f / aspect_ratio, 0, 0, 0],
    [0, f, 0, 0],
    [0, 0, (far + near) / (far - near), 1],
    [0, 0, (-2 * far * near) / (far - near), 0]
  ])

collisions = {
  'right_collision' :  False,
  'left_collsion'  :  False,
  'bottom_collision' : False,
  'top_collision'    : False,
  'near_collision'   : False,
  'far_collsion'     : False
}

def check_collisions(cube_points, movement_vector, flags):
  for point in cube_points:
      if point[0] >= SCREEN_WIDTH and not flags['right_collision']:
        flags['right_collision'] = True
        flags['left_collsion'] = False
        movement_vector[0] *= -1
      elif point[0] <= 0 and not flags['left_collsion']:
        flags['left_collsion'] = True
        flags['right_collision'] = False
        movement_vector[0] *= -1
      if point[1] >= SCREEN_HEIGHT and not flags['bottom_collision']:
        flags['bottom_collision'] = True
        flags['top_collision'] = False
        movement_vector[1] *= -1
      elif point[1] <= 0 and not flags['top_collision']:
        flags['top_collision'] = True
        flags['bottom_collision'] = False
        movement_vector[1] *= -1
      if point[2] >= MAX_Z and not flags['far_collsion']:
        flags['far_collision'] = True
        flags['near_collision'] = False
        movement_vector[2] *= -1
      elif point[2] <= MIN_Z and not flags['near_collision']:
        flags['near_collision'] = True
        flags['far_collision'] = False
        movement_vector[2] *= -1

cube_points = cube_points@enlarge
cube_points = cube_points@translation_matrix

# camera position
camera_position = np.array([200, 150, -10, 0])

# rotation matrices
x_rotation_matrix = create_xrotation_matrix(pi/100)
y_rotation_matrix = create_yrotation_matrix(pi/100)
z_rotation_matrix = create_zrotation_matrix(pi/100)

# center
center = np.mean(cube_points[:, :3], axis=0)

# incorporate center
def rotate_around_center(points, angle_x, angle_y, angle_z, center):
    translation_to_origin = np.eye(4)
    translation_to_origin[:3, 3] = -center
    translation_back = np.eye(4)
    translation_back[:3, 3] = center
    
    x_rotation = create_xrotation_matrix(angle_x)
    y_rotation = create_yrotation_matrix(angle_y)
    z_rotation = create_zrotation_matrix(angle_z)

    rotation_matrix = translation_back @ z_rotation @ y_rotation @ x_rotation @ translation_to_origin

    return (points @ rotation_matrix.T)

# perspective projection matrix
perspective_projection_matrix = create_perspective_projection_matrix(60, SCREEN_WIDTH / SCREEN_HEIGHT, 0.1, 1000)

movement_vector = np.array([randint(-2, 2), randint(-2, 2), 0, 0])

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()

    cube_points += movement_vector
    center += movement_vector[:3]
  
    # rotate cube
    #rotated_points = rotate_around_center(cube_points, pi/100, pi/100, pi/100, center)

    rotated_points = cube_points@x_rotation_matrix@y_rotation_matrix@z_rotation_matrix

    # check for collisions
    check_collisions(rotated_points, movement_vector, collisions)

    # apply view transformation
    view_points = rotated_points - camera_position

    # apply perspective projection
    projected_points = view_points@perspective_projection_matrix.T
    projected_points /= projected_points[:, 3, np.newaxis]

    # translate to screen coordinates
    screen_points = projected_points + np.array([SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 0, 0])

    # redraw bg
    DISPLAYSURF.fill((0, 0, 0))
  
    for idx in cube_indices:
      pygame.draw.line(DISPLAYSURF, (255, 0, 0), (screen_points[idx[0]][0], screen_points[idx[0]][1]), (screen_points[idx[1]][0], screen_points[idx[1]][1]))

    time.sleep(.1)
      
    pygame.display.update()
