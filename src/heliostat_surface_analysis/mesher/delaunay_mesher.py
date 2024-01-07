from typing import Tuple, Union, Optional, cast, Any, Dict

import numpy as np
from stl.mesh import Mesh
from scipy.spatial import Delaunay

from heliostat_surface_analysis.mesher.mesher import Mesher


class DelaunayMesher(Mesher):
    def __init__(self, params: Optional[Dict[str, Union[str, float]]],):
        self.max_aspect_ratio = params["max_aspect_ratio"]
        
    def create_mesh(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> Tuple[Mesh, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        tris = self.points_to_tris(x, y)
        return self.points_and_tris_to_mesh(x, y, z, tris)

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
        tris.simplices = self.filter_triangles(tris)
        if len(tris.simplices)==0:
            raise RuntimeError("no simplices after filtering Delaunay triangulation")
        return tris

    def filter_triangles(
        self,
        tris: Delaunay,
    ) -> np.ndarray:
        small_tris = []
        for tri in tris.simplices:
            p0 = tris.points[tri[0]]
            p1 = tris.points[tri[1]]
            p2 = tris.points[tri[2]]
            # side lengths
            a = np.linalg.norm(p0 - p1)
            b = np.linalg.norm(p1 - p2)
            c = np.linalg.norm(p2 - p0)
            # aspect ratio (see https://stackoverflow.com/questions/10289752/aspect-ratio-of-a-triangle-of-a-meshed-surface)
            s = (a + b + c) / 2.0
            aspect_ratio = (a * b * c) / (8.0 * (s - a) * (s - b) * (s - c))
            if aspect_ratio < self.max_aspect_ratio:
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
