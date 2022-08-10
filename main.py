import laspy
import numpy as np
import open3d as o3d

las_file = laspy.read('2743_1234.las')

data = np.stack([las_file.X, las_file.Y, las_file.Z], axis=0).T

geom = o3d.geometry.PointCloud()
geom.points = o3d.utility.Vector3dVector(data)
geom.colors = o3d.utility.Vector3dVector(np.random.uniform(0, 1, size=(las_file.header.point_count, 3)))

octree = o3d.geometry.Octree(max_depth=10)
octree.convert_from_point_cloud(geom)

o3d.visualization.draw_geometries([octree])
