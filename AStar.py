from Octree import Octree


def can_go_to_point(octree: Octree, point) -> bool:
    if octree.childs:
        for child in octree.childs:
            if child.collide_point(point):
                return can_go_to_point(child, point)
    elif octree.points:
        return False
    return True


def xyz_to_x0y0z0(xyz, cube):
    # x = xyz[0]
    # x0 = x0y0z0[0][0]
    # w = x0y0z0[1]
    # x = (x - x0 + x0 // w * w) // w * w + x0 - x0 // w * w
    return tuple(
        [
            round(((xyz[i] - cube[0][i] + cube[0][i] // cube[1] * cube[1])
                    // cube[1] * cube[1] + cube[0][i] - cube[0][i] // cube[1] * cube[1]), 3)
            for i in range(3)
        ]
    )


class Node:
    def __init__(self):
        self.x0y0z0 = None
        self.previous = None
        self.xyz = None
        self.cost = 1_000_000_000
        self.dist = None

    def __eq__(self, other):
        x1, y1, z1 = self.x0y0z0
        x2, y2, z2 = other.x0y0z0

        if round(x1 - x2, 3) == round(y1 - y2, 3) == round(z1 - z2, 3) == 0:
            return True

        return False

    def __hash__(self):
        return hash(self.x0y0z0)


class AStar:
    def __init__(self, start: tuple, goal: tuple, oct_cube, octree: Octree):
        self.start = Node()
        self.start.x0y0z0 = xyz_to_x0y0z0(start, oct_cube)
        self.start.xyz = start
        self.start.cost = 0

        self.goal = Node()
        self.goal.x0y0z0 = xyz_to_x0y0z0(goal, oct_cube)
        self.goal.xyz = goal

        self.start.dist = self.distance_to_goal(self.start)

        self.step = oct_cube[1]
        self.octree = octree

    def distance_to_goal(self, node):
        x0, y0, z0 = node.x0y0z0
        x1, y1, z1 = self.goal.x0y0z0
        return (x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2

    def find_path(self):
        reachable = {self.start}
        explored = set()

        while reachable:
            node = reachable.pop()
            reachable.add(node)

            for pos_node in reachable:

                if pos_node.dist + pos_node.cost < node.dist + node.cost:
                    node = pos_node
                elif pos_node.dist < node.dist and pos_node.dist + pos_node.cost == node.dist + node.cost:
                    node = pos_node

            if node == self.goal:
                self.goal = node
                return self.get_path_cubes()

            explored.add(node)
            reachable.remove(node)

            for adj in (self.adjacent_to_node(node) - explored):

                reachable.add(adj)
                adj.dist = self.distance_to_goal(adj)

                if node.cost + self.step < adj.cost:
                    adj.previous = node
                    adj.cost = node.cost + self.step

        return None

    def adjacent_to_node(self, node):
        nodes = set()
        x, y, z = node.xyz
        x0, y0, z0 = node.x0y0z0

        for i in range(-1, 2, 2):
            for j in range(3):

                coord = [x, y, z]
                coord[j] += self.step * i

                if can_go_to_point(self.octree, coord):
                    pos_node = Node()
                    pos_node.xyz = tuple(coord)

                    coord_cube = [x0, y0, z0]
                    coord_cube[j] += self.step * i
                    pos_node.x0y0z0 = tuple(coord_cube)

                    nodes.add(pos_node)

        return nodes

    def get_path_cubes(self):
        path = list()
        to_node = self.goal

        while to_node is not None:
            path.append((to_node.x0y0z0, self.step))
            to_node = to_node.previous

        return path
