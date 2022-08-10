import Octree as oct
from numpy.random import randint
import numpy as np
from DrawCube import DrawCube
import laspy
from math import log2
from math import ceil


las_file = laspy.read('2743_1234.las')
points = np.stack([las_file.X, las_file.Y, las_file.Z], axis=0).T

w = 2 ** ceil(log2(max(las_file.X + las_file.Y + las_file.Z)))
# points = randint(0, 2 ** 10, size=(10000, 3))
# w = 1024
octree = oct.Octree((0, 0, 0, w, w, w), points=points, max_depth=2)
oct.self_build(octree)

# oct.print_octree(octree, 0)

draw_cube = DrawCube()
draw_cube.get_octree(octree)
draw_cube.draw_cubes()

