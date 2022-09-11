from Octree import Octree


def can_go_to_point(octree: Octree, point: tuple):
    if octree.childs:
        for child in octree.childs:
            if child.collide_point(point):
                return can_go_to_point(child, point)
    elif octree.points:
        return False
    return True


def xyz_to_cube(xyz, cube):
    x, y, z = xyz
    x0, y0, z0 = cube[0]
    w = cube[1]
    x = (x - x0 + x0 // w * w) // w * w + x0 - x0 // w * w
    y = (y - y0 + y0 // w * w) // w * w + y0 - y0 // w * w
    z = (z - z0 + z0 // w * w) // w * w + z0 - z0 // w * w
    return (round(x, 3), round(y, 3), round(z, 3)), w


class Node:
    def __init__(self):
        self.cube = None
        self.previous = None
        self.xyz = None
        self.cost = 9999999999

    def __eq__(self, other):
        x1, y1, z1 = self.cube
        x2, y2, z2 = other.cube
        if round(x1 - x2, 3) == round(y1 - y2, 3) == round(z1 - z2, 3) == 0:
            return True
        return False

    def __hash__(self):
        return hash(self.cube)


class AStar:
    def __init__(self, start: tuple, destiny: tuple, oct_cube, octree, start_color=(0, 0, 1), destiny_color=(1, 0, 0)):
        self.start = Node()
        self.start.cube = xyz_to_cube(start, oct_cube)[0]
        self.start.xyz = start
        self.start.cost = 0

        self.destiny = Node()
        self.destiny.cube = xyz_to_cube(destiny, oct_cube)[0]
        self.destiny.xyz = destiny

        self.start_color = start_color
        self.destiny_color = destiny_color

        self.step = oct_cube[1]
        self.octree = octree

    def distance_to_destiny(self, node):
        x0, y0, z0 = node.cube
        x1, y1, z1 = self.destiny.cube
        return (x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2

    def find_path(self):
        reachable = {self.start}
        explored = set()

        while reachable:
            node = list(reachable)[0]
            for pos_node in reachable:
                pos_cost = self.distance_to_destiny(pos_node)
                node_cost = self.distance_to_destiny(node)
                if pos_cost + pos_node.cost < node_cost + node.cost:
                    node = pos_node
                elif pos_cost < node_cost:
                    node = pos_node

            print(node.cube, node.cost, self.distance_to_destiny(node))

            if node == self.destiny:
                self.destiny = node
                return self.get_path_cubes()

            explored.add(node)
            reachable.remove(node)

            for adj in (self.nodes_can_go(node) - explored):
                reachable.add(adj)
                if node.cost + self.step < adj.cost:
                    adj.previous = node
                    adj.cost = node.cost + self.step
        return None

    def nodes_can_go(self, node):
        nodes = set()
        x, y, z = node.xyz
        x0, y0, z0 = node.cube
        for i in range(-1, 2, 2):
            for j in range(3):
                coord = [x, y, z]
                coord[j] += self.step * i
                coord = tuple(coord)
                if can_go_to_point(self.octree, coord):
                    pos_node = Node()
                    pos_node.xyz = coord
                    coord_cube = [x0, y0, z0]
                    coord_cube[j] += self.step * i
                    pos_node.cube = tuple(coord_cube)
                    nodes.add(pos_node)
                else:
                    print(1)
        return nodes

    def get_path_cubes(self):
        path = list()
        to_node = self.destiny
        while to_node is not None:
            path.append((to_node.cube, self.step))
            to_node = to_node.previous
        return path
