import numpy as np
import open3d as o3d


class Cubes:
    def __init__(self):
        with open('points.txt') as f:
            self.base_dtp = [[int(i) for i in j.split()] for j in f.readlines()]

        with open('triangles.txt') as g:
            self.base_faces = [[int(i) for i in j.split()] for j in g.readlines()]
        self.dtp = []
        self.faces = []
        self.mesh = o3d.geometry.TriangleMesh()
        self.k = 0

    def add_cube(self, xyz0, w):
        self.dtp += [[j[i] * w + xyz0[i] for i in range(3)] for j in self.base_dtp]
        self.faces += [[j[i] + 8 * self.k for i in range(3)] for j in self.base_faces]
        self.k += 1

    def draw(self, l):
        self.mesh.vertices = o3d.utility.Vector3dVector(self.dtp)
        self.mesh.triangles = o3d.utility.Vector3iVector(self.faces)
        self.mesh.vertex_colors = o3d.utility.Vector3dVector(np.concatenate(
            (np.random.uniform(0.4, 0.6,size=((self.k - 2) * 8, 3)), np.array([[1, 0, 0]] * 8 + [[0, 0, 1]] * 8)), axis=0))
        return self.mesh
