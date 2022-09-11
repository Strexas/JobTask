import open3d as o3d


class Cubes:
    def __init__(self):
        with open('points.txt') as f:
            self.base_dtp = [[int(i) for i in j.split()] for j in f.readlines()]

        with open('triangles.txt') as g:
            self.base_faces = [[int(i) for i in j.split()] for j in g.readlines()]

        self.dtp = []
        self.faces = []
        self.colors = []

        self.k = 0

        self.mesh = o3d.geometry.TriangleMesh()

    def add_cube(self, cube):
        x0y0z0 = cube[0]
        w = cube[1]

        self.dtp += [[j[i] * w + x0y0z0[i] for i in range(3)] for j in self.base_dtp]
        self.faces += [[j[i] + 8 * self.k for i in range(3)] for j in self.base_faces]

        self.k += 1

    def add_cubes(self, cubes):
        for cube in cubes:
            self.add_cube(cube)

    def __add__(self, other):
        new = Cubes()
        new.dtp = self.dtp + other.dtp
        new.faces = self.faces + other.faces
        new.colors = self.colors + other.colors
        new.k = self.k + other.k
        return new

    def draw(self):
        self.mesh.vertices = o3d.utility.Vector3dVector(self.dtp)
        self.mesh.triangles = o3d.utility.Vector3iVector(self.faces)
        self.mesh.vertex_colors = o3d.utility.Vector3dVector(self.colors)
        o3d.visualization.draw_geometries([self.mesh])
