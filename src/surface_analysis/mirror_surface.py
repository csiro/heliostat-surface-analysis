from dataclasses import dataclass

import pandas as pd
from scipy.spatial import Delaunay
from stl import mesh


@dataclass
class MirrorSurface:
    name: str
    design_focal_length: float
    points: pd.DataFrame
    tris: Delaunay
    mesh: mesh.Mesh
    facets: pd.DataFrame
    uncertainties: bool = False
