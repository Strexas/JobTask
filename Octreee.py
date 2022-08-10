class Octree:
    def __init__(self, octant, parent=None, points=set(), max_depth=4):
        self.points = set([tuple(i) for i in points])
        self.octant = octant
        self.childs = set()
        self.parent = parent
        self.max_depth = max_depth

    def collide(self, point):
        x0, y0, z0, x1, y1, z1 = self.octant
        if x0 <= point[0] <= x1 and y0 <= point[1] <= y1 and z0 <= point[2] <= z1:
            return True
        else:
            return False


def self_build(octree):
    if not octree.max_depth or len(octree.points) <= 1:
        return

    w = (octree.octant[3] - octree.octant[0]) // 2
    x0, y0, z0 = octree.octant[:3]

    for x in range(2):
        for y in range(2):
            for z in range(2):
                octree.childs.add(Octree((x0 + x * w, y0 + y * w, z0 + z * w,
                                          x0 + (x + 1) * w, y0 + (y + 1) * w, z0 + (z + 1) * w),
                                         octree, max_depth=octree.max_depth - 1))

    for child in octree.childs:
        for point in list(octree.points):
            if child.collide(point):
                child.points.add(point)
                octree.points.remove(point)

    for child in list(octree.childs):
        if len(child.points) == 0:
            octree.childs.remove(child)

    for child in octree.childs:
        self_build(child)


def print_octree(octree, k):
    if not octree.max_depth:
        print('\t' * k, 'deepest child')
        return
    print('\t' * k, k, 'layer of tree with', len(octree.childs), 'childs:')
    for child in octree.childs:
        print_octree(child, k + 1)
