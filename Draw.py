import open3d as o3d


def draw(*args):
    o3d.visualization.draw_geometries([*args])
