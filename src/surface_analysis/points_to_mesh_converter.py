from stl.mesh import Mesh
import pandas as pd
from scipy.spatial import Delaunay
import numpy as np


DEFAULT_MAX_EDGE_LENGTH = 0.2


class PointsToMeshConverter:
    @staticmethod
    def points_to_tris(
        points: pd.DataFrame, max_edge_length: float = DEFAULT_MAX_EDGE_LENGTH
    ) -> Delaunay:
        """
        Apply Delaunay triangulation to the point cloud only using x and y values.
        Filter out erroneous large triangles along the edges.
        """
        xy_points = points[["x", "y"]].to_numpy()
        tris = Delaunay(xy_points)
        tris.simplices = PointsToMeshConverter.filter_short_tris(tris, max_edge_length)
        return tris

    @staticmethod
    def filter_short_tris(tris: Delaunay, max_edge_length: float) -> np.array:
        small_tris = []
        for tri in tris.simplices:
            p0 = tris.points[tri[0]]
            p1 = tris.points[tri[1]]
            p2 = tris.points[tri[2]]
            longest_side = max(
                np.linalg.norm(p0 - p1),
                np.linalg.norm(p1 - p2),
                np.linalg.norm(p2 - p0),
            )
            if longest_side < max_edge_length:
                small_tris.append(tri)

        return np.array(small_tris)

    @staticmethod
    def points_and_tris_to_mesh(points: pd.DataFrame, tris: Delaunay) -> Mesh:
        """
        Create a Mesh object from the Delaunay triangulation.
        Delauney stores each triangle's points by index but Mesh stores them by the whole vector.
        """
        xyz_points = points[["x", "y", "z"]].to_numpy()

        mesh = Mesh(np.zeros(tris.simplices.shape[0], dtype=Mesh.dtype))
        for i in range(tris.simplices.shape[0]):
            tri = tris.simplices[i]
            for j in range(tris.simplices.shape[1]):
                point_index = tri[j]
                point_vector = xyz_points[point_index, :]
                mesh.vectors[i][j] = point_vector

        mesh.update_normals()
        return mesh

    @staticmethod
    def mesh_to_facets(mesh: Mesh) -> pd.DataFrame:
        """
        Make a dataframe for each tri in the Mesh.
        Store its centroid and unit normal too.
        """
        facets = pd.DataFrame(
            data=mesh.points,
            dtype=float,
            columns=["x1", "y1", "z1", "x2", "y2", "z2", "x3", "y3", "z3"],
        )
        facets["x"] = facets[["x1", "x2", "x3"]].mean(axis=1)
        facets["y"] = facets[["y1", "y2", "y3"]].mean(axis=1)
        facets["z"] = facets[["z1", "z2", "z3"]].mean(axis=1)

        unit_normals = mesh.normals / np.linalg.norm(mesh.normals)
        normals = pd.DataFrame(unit_normals, columns=["nx", "ny", "nz"])

        return pd.concat([facets, normals], axis=1)
