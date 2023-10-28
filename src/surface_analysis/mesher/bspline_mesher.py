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

    def create_mesh(
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

        return self.points_and_tris_to_mesh(xi, yi, zi, tris)
        
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
