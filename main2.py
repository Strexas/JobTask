import Octree as oct
import numpy as np
from Cubes import Cubes
import laspy


las_file = laspy.open('2743_1234.las')
read_data = las_file.read()

points = read_data.xyz
w = 2 ** np.ceil(np.log2(np.max(points)))
org = np.min(points)
np.shuffle(points)

# points = randint(0, 2 ** 10, size=(10, 3))
# w = 1024

octree = oct.Octree((org, org, org, w + org, w + org, w + org), points=points[:100000], max_depth=20)
oct.self_build(octree)
print("octree has built")

# oct.print_octree(octree)

draw_octree = Cubes()

full_octree_cubes = oct.get_octree(octree)

for cube in full_octree_cubes:
    draw_octree.add_cube(cube[0], cube[1])

draw_octree.draw_cubes()

