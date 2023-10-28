from typing import Tuple, Union, Optional, cast, Any, Dict, List

import numpy as np
import pandas as pd
from stl.mesh import Mesh

import numpy as np
from scipy import interpolate

from surface_analysis.vector_math import area_of_triangles, area_of_triangles_xy
from surface_analysis.mesher.mesher import Mesher


class BSplineMesher(Mesher):
    def __init__(self, params: Optional[Dict[str, Union[str, float]]],):
        self.polynomial_degree = int(params["polynomial_degree"])
        # self.smoothing_factor = params["smoothing_factor"]
        self.dx = params["dx"]
        self.dy = params["dy"]

    def points_to_facets(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> Tuple[Mesh, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        # NOTE: best results seemed to be obtained when the smoothing factor is automatically determined
        tck = interpolate.bisplrep(x, y, z, kx=self.polynomial_degree, ky=self.polynomial_degree) # , s=self.smoothing_factor)
        
        xmin = x.min()
        xmax = x.max()
        ymin = y.min()
        ymax = y.max()
        
        nx = int(round((xmax - xmin) / self.dx))
        xi = np.linspace(xmin,xmax,nx)
        
        ny = int(round((ymax - ymin) / self.dy))
        yi = np.linspace(ymin,ymax,ny)
        
        zi = interpolate.bisplev(xi,yi,tck)
        
        # FIXME: might be a more pythonic way to do this 
        # NOTE: order of vertices is important to get direction of normal correct
        tris = []
        for i in range(nx-1):
            for j in range(ny-1):
                v1 = [i,j]
                v2 = [i+1,j+1]
                v3 = [i,j+1]
                tris.append([v1,v2,v3])
                v1 = [i,j]
                v2 = [i+1,j]
                v3 = [i+1,j+1]
                tris.append([v1,v2,v3])

        mesh = self.points_and_tris_to_mesh(xi, yi, zi, tris)
        facets = self.mesh_to_facets(mesh)
        return (
			mesh,
            facets["x"].to_numpy().reshape(-1, 1),
            facets["y"].to_numpy().reshape(-1, 1),
            facets["z"].to_numpy().reshape(-1, 1),
            facets["area"].to_numpy().reshape(-1, 1),
            facets[["nx", "ny", "nz"]].to_numpy(),
        )
        
    def points_and_tris_to_mesh(
        self,
        x: np.ndarray,  # nx1
        y: np.ndarray,  # mx1
        z: np.ndarray,  # nxm
        tris: List,
    ) -> Mesh:
        """
        Create a Mesh object.
        """

        mesh = Mesh(np.zeros(len(tris), dtype=Mesh.dtype))
        for i in range(len(tris)):
            # NOTE: tri is a list of the vertex indices
            tri = tris[i]
            for j in range(len(tri)):
                point_indices = tri[j]
                mesh.vectors[i][j] = np.array([x[point_indices[0]],y[point_indices[1]],z[point_indices[0],point_indices[1]]])
        
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