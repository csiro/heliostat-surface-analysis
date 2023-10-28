from abc import ABC, abstractmethod

import numpy as np
from stl.mesh import Mesh
import typing
import pandas as pd

from surface_analysis.vector_math import area_of_triangles, area_of_triangles_xy

class Mesher(ABC):
    @abstractmethod
    def create_mesh(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> Mesh:
        pass

    @staticmethod
    def get_facets(mesh: Mesh) -> typing.Tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]:
        """
        Return the centroid, area and normal vector components for each triangle in the Mesh
        """
        
        # FIXME: should probably do this without pandas 
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

        facets = pd.concat([facets, normals, areas, areas_xy], axis=1)
        return (
            facets["x"].to_numpy().reshape(-1, 1),
            facets["y"].to_numpy().reshape(-1, 1),
            facets["z"].to_numpy().reshape(-1, 1),
            facets["area"].to_numpy().reshape(-1, 1),
            facets[["nx", "ny", "nz"]].to_numpy(),
        )