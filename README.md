# Introduction
I made this a way to explore making a 3d wireframe cube that rotates and bounces around the screen. Currently it can bounce off the sides but wventually I want to add depth and the ability for the cube to bounce off a wall in the z space and utilize scaling to simulate the depth. 

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
])'

to be continued...