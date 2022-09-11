import Octree as oct
import numpy as np
from Cubes import Cubes
import laspy
from AStar import AStar, xyz_to_cube, can_go_to_point
from Draw import draw

np.random.seed(1)

las_file = laspy.open('2743_1234.las')
read_data = las_file.read()

points = read_data.xyz
w = 2 ** np.ceil(np.log2(np.max(points)))
org = np.min(points)
np.random.shuffle(points)

# points = randint(0, 2 ** 10, size=(10, 3))
# w = 1024

octree = oct.Octree((org, org, org, w + org, w + org, w + org), points=points[:10000000], max_depth=20)
oct.self_build(octree)
print("octree has built")

# oct.print_octree(octree)

draw_octree = Cubes()

full_octree_cubes = list(oct.get_octree(octree))

for cube in full_octree_cubes:
    draw_octree.add_cube(cube[0], cube[1])

print('A has started')
A_cubes = [1, 2]

A = AStar((2743856, 1234060, 1920), (2743056, 1234940, 1992), full_octree_cubes[0], octree)
print(A.start.cube)
print(A.destiny.cube)
A_cubes = A.find_path()

for cube in A_cubes:
    draw_octree.add_cube(cube[0], cube[1])


print('END')
draw(draw_octree.draw(len(A_cubes)))
