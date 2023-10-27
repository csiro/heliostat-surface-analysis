from typing import Tuple, Union, Optional, cast, Any, Dict

import numpy as np
import pandas as pd
from stl.mesh import Mesh
from scipy.spatial import Delaunay

from surface_analysis.vector_math import area_of_triangles, area_of_triangles_xy
from surface_analysis.mesher.mesher import Mesher


class DelaunayMesher(Mesher):
    def __init__(self, params: Optional[Dict[str, Union[str, float]]],):
        self.max_edge_length = params["max_edge_length"]

    def points_to_facets(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> Tuple[Mesh, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        tris = self.points_to_tris(x, y)

        mesh = self.points_and_tris_to_mesh(x, y, z, tris)
        facets = self.mesh_to_facets(mesh)
        return (
			mesh,
            facets["x"].to_numpy().reshape(-1, 1),
            facets["y"].to_numpy().reshape(-1, 1),
            facets["z"].to_numpy().reshape(-1, 1),
            facets["area"].to_numpy().reshape(-1, 1),
            facets[["nx", "ny", "nz"]].to_numpy(),
        )

    def points_to_tris(
        self,
        x: np.ndarray,
        y: np.ndarray,
    ) -> Delaunay:
        """
        Apply Delaunay triangulation to the point cloud only using x and y values.
        Filter out erroneous large triangles along the edges.
        """
        xy = np.hstack([x, y])
        tris = Delaunay(xy)
        tris.simplices = self.filter_short_tris(tris, self.max_edge_length)
        if len(tris.simplices)==0:
            raise RuntimeError("no simplices after filtering Delaunay triangulation")
        return tris

    def filter_short_tris(
        self,
        tris: Delaunay,
        max_edge_length: float
    ) -> np.ndarray:
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

    def points_and_tris_to_mesh(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        tris: Delaunay,
    ) -> Mesh:
        """
        Create a Mesh object from the Delaunay triangulation.
        Delaunay stores each triangle's points by index but Mesh stores them by the whole vector.
        """
        xyz = np.hstack([x, y, z])

        mesh = Mesh(np.zeros(tris.simplices.shape[0], dtype=Mesh.dtype))
        for i in range(tris.simplices.shape[0]):
            tri = tris.simplices[i]
            for j in range(tris.simplices.shape[1]):
                point_index = tri[j]
                point_vector = xyz[point_index, :]
                mesh.vectors[i][j] = point_vector

        mesh.update_normals()
        return mesh

    def mesh_to_facets(self, mesh: Mesh) -> pd.DataFrame:
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

        p1 = facets[["x1", "y1", "z1"]].to_numpy()
        p2 = facets[["x2", "y2", "z2"]].to_numpy()
        p3 = facets[["x3", "y3", "z3"]].to_numpy()
        areas = pd.DataFrame(area_of_triangles(p1, p2, p3), columns=["area"])
        areas_xy = pd.DataFrame(area_of_triangles_xy(p1, p2, p3), columns=["area_xy"])

        unit_normals = mesh.normals / np.linalg.norm(mesh.normals)
        normals = pd.DataFrame(unit_normals, columns=["nx", "ny", "nz"])

        return pd.concat([facets, normals, areas, areas_xy], axis=1)
