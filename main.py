print('Presets: ', end='')

points_amount = 10_000_000  # max ~ 20_000_000, live None to use all points
shuffle_data = True
max_depth = 20

print('FINISHED')


print('Importing: ', end='')

import Octree as oct
import numpy as np
from Cubes import Cubes
import laspy
from AStar import AStar

print('FINISHED')

print('Reading data: ', end='')

las_file = laspy.open('2743_1234.las')
read_data = las_file.read()

points = read_data.xyz
w = 2 ** np.ceil(np.log2(np.max(points)))
org = np.min(points)

print('FINISHED')


if shuffle_data:
    print('Shuffling data: ', end='')

    np.random.seed(1)
    np.random.shuffle(points)

    print('FINISHED')


print('Building Octree: ', end='')

if points_amount is None:
    points_amount = las_file.header.point_count
else:
    try:
        assert points_amount <= las_file.header.point_count
    except AssertionError as e:
        raise Exception('Too much points :)')

octree = oct.Octree((org, org, org, w + org, w + org, w + org), points=points[:points_amount], max_depth=max_depth)
oct.self_build(octree)

print("FINISHED")


print('Building Octree\'s Mesh: ', end='')

full_octree_cubes = list(oct.get_octree(octree))

draw_octree = Cubes()
draw_octree.add_cubes(full_octree_cubes)
draw_octree.colors = list(np.random.uniform(0.5, 0.7, size=(draw_octree.k * 8, 3)))

print('FINISHED')


print('Startin A*: ', end='')

start_point = (2743856, 1234060, 1920)
goal_point = (2743056, 1234940, 1992)
A = AStar(start_point, goal_point, full_octree_cubes[0], octree)

A_cubes = A.find_path()

print('FINISHED')


print('Building A*\'s Mesh: ', end='')

draw_A = Cubes()
draw_A.add_cubes(A_cubes)
draw_A.colors = [[1, 0, 0]] * 8 + [[0, 1, 0]] * 8 * (draw_A.k - 2) + [[0, 0, 1]] * 8

print('FINISHED')


print('Drawing Octree and Path: ', end='')

(draw_A + draw_octree).draw()

print('FINISHED')
