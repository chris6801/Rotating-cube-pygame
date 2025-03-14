# Introduction
I made this a way to explore making a 3d wireframe cube that rotates and bounces around the screen. Currently it can bounce off the sides but wventually I want to add depth and the ability for the cube to bounce off a wall in the z space and utilize scaling to simulate the depth. 

![RPReplay_Final1730154781](https://github.com/user-attachments/assets/2ca2f50e-0c0f-4605-a41c-49f64f4a418f)

## Installation 
You'll need python obviously. You can download the latest version here:
https://www.python.org/downloads/

This program uses NumPy and PyGame as dependencies. Using pip you can install them with:

`pip install numpy`

`pip install pygame`



## Storing the cube
The cube is stored as a numpy array of each x,y,z point and another numpy array of indices into the points array to describe how to connect each point for each edge of the cube. 

### The points
`cube_points = np.array([
    [0, 1, 1],
    [0, 0, 1],
    [0, 0, 0],
    [0, 1, 0],
    [1, 1, 1],
    [1, 0, 1],
    [1, 0, 0],
    [1, 1, 0]
])`

### The edge indices
`cube_indices = np.array([
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
])`

## Scaling and translating the cube
We will use a scaling matrix to multiply every point by 50 to make the cube more easily visible. The @ in numpy is a shorthand for matrix multiplication.

Then we will translate the cube by 150 in the x direction and 200 in the y direction to center the cube on the screen somewhat. This is done by adding the vector to the matrix.
`#enlarge cube
enlarge = np.array([
    [50,  0,  0],
    [ 0, 50,  0],
    [ 0,  0, 50]
])`

`# translation vector 
translation = np.array([
[150, 200, 0]
])`

`cube_points = cube_points@enlarge
cube_points += translation`

## Drawing the cube 
First we need to set up our window (or display surface). 

`SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300`

`pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hello World!')`

Then we will use the pygame line function to draw a line. We simply iterate through our edge indice array and draw a line between each point based on index pairs. 
`DISPLAYSURF.fill((0, 0, 0))`
  
`    for idx in cube_indices:
      pygame.draw.line(DISPLAYSURF, (255, 0, 0), (points_2d[idx[0]][0], points_2d[idx[0]][1]), (points_2d[idx[1]][0], points_2d[idx[1]][1]))`
