import Octree as oct
import numpy as np
from Cubes import Cubes
import laspy
from AStar import AStar
from Draw import draw

las_file = laspy.open('2743_1234.las')
read_data = las_file.read()

points = read_data.xyz
w = 2 ** np.ceil(np.log2(np.max(points)))
org = np.min(points)
np.random.shuffle(points)

# points = randint(0, 2 ** 10, size=(10, 3))
# w = 1024

octree = oct.Octree((org, org, org, w + org, w + org, w + org), points=points[:1000000], max_depth=20)
oct.self_build(octree)
print("octree has built")

# oct.print_octree(octree)

draw_octree = Cubes()

full_octree_cubes = list(oct.get_octree(octree))

for cube in full_octree_cubes:
    draw_octree.add_cube(cube[0], cube[1])


A_cubes = []

draw_octree.add_cube((2743698.8 + 40 * 4, 1234022.8 + 10 * 4, 1874.8 + 12 * 4), 4)
draw_octree.add_cube((2743698 - 160 * 4, 1234022 + 230 * 4, 1874.8 + 30 * 4), 4)
# print('A has started')
# A = AStar((0, 0, 0), (10000, 10000, 10000), list(full_octree_cubes)[0], octree)
#
# A_cubes = A.find_path()
#
# for cube in A_cubes:
#     draw_octree.add_cube(cube[0], cube[1])
#
# print('END')
draw(draw_octree.draw(len(A_cubes)))
