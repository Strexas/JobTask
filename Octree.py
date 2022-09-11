class Octree:
    def __init__(self, octant: tuple, parent=None, points=None, max_depth: int = 4) -> None:
        if points is None:
            self.points: set = set()
        elif points is not set:
            self.points: set = {tuple(i) for i in points}
        else:
            self.points: set = points
        self.octant: tuple = octant
        self.childs: set = set()
        self.parent: Octree = parent
        self.max_depth: int = max_depth

    def collide_point(self, point):
        x0, y0, z0, x1, y1, z1 = self.octant
        if x0 <= point[0] <= x1 and y0 <= point[1] <= y1 and z0 <= point[2] <= z1:
            return True
        else:
            return False


def self_build(octree):
    if not octree.max_depth:
        if not octree.points:
            octree.parent.childs.remove(octree)
        return

    w = (octree.octant[3] - octree.octant[0]) // 2  # new octant's width = (x1 - x0) // 2
    x0, y0, z0 = octree.octant[:3]

    for x in range(2):
        for y in range(2):
            for z in range(2):
                octree.childs.add(Octree((x0 + x * w, y0 + y * w, z0 + z * w,
                                          x0 + (x + 1) * w, y0 + (y + 1) * w, z0 + (z + 1) * w),
                                         octree, max_depth=octree.max_depth - 1))

    for child in octree.childs:
        for point in octree.points.copy():
            if child.collide_point(point):
                child.points.add(point)
        octree.points -= child.points

    for child in octree.childs.copy():
        if child.points:
            self_build(child)


def get_octree(octree: Octree) -> set:
    st = set()

    def get_child(octree: Octree) -> None:
        if len(octree.points) >= 1:
            st.add((octree.octant[:3], octree.octant[3] - octree.octant[0]))

        for child in octree.childs:
            get_child(child)

    get_child(octree)

    return st


def print_octree(octree: Octree, k=0) -> None:
    if not octree.max_depth:
        print('\t' * k, f'deepest child: {len(octree.points)}')
        return
    print('\t' * k, k, 'layer of tree with', len(octree.childs), 'childs:')
    for child in octree.childs:
        print_octree(child, k + 1)
