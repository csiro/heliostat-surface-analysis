import pandas as pd
import numpy as np

from surface_analysis.mirror_surface import MirrorSurface
from surface_analysis.points_to_mesh_converter import PointsToMeshConverter


class Loader:
    def from_leica(self, file_path: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Load a leica point cloud and just return the x,y,z
        """
        points = self.load_leica_points(file_path)
        return (
            points["x"].to_numpy().reshape(-1, 1),
            points["y"].to_numpy().reshape(-1, 1),
            points["z"].to_numpy().reshape(-1, 1),
        )

    def load_leica_points(self, file_path: str) -> pd.DataFrame:
        """
        Load Leica
        Leica data includes uncertainty and has been pre-orientated.
        """
        points = pd.read_csv(
            file_path,
            skiprows=7,
            delimiter=",  ",
            header=None,
            engine="python",
        )
        points = self.cleanup_leica_columns(points)
        return self.scale_mm_to_m(points)

    def cleanup_leica_columns(self, points: pd.DataFrame) -> pd.DataFrame:
        """Drop unnecessary Leica columns and label remaining ones."""
        points = points.copy()
        columns_to_drop = list(range(4, 6)) + list(range(9, len(points.columns)))
        points.drop(
            points.columns[columns_to_drop],
            axis=1,
            inplace=True,
        )

        points.columns = ["index", "x", "y", "z", "del_x", "del_y", "del_z"]
        points = points.set_index("index")
        return points

    def scale_mm_to_m(self, points: pd.DataFrame) -> pd.DataFrame:
        points = points.copy()
        points /= 1000
        return points

    # def from_leica_old(
    #     self, name: str, design_focal_length: float, file_path: str
    # ) -> MirrorSurface:
    #     """
    #     Loads a pointcloud data file from the Leica Absolute Tracker.
    #     Pre-processes it to create mesh data as well.
    #     """
    #     p2m = PointsToMeshConverter()
    #     points = self.load_leica_points(file_path)
    #     tris = p2m.points_to_tris_old(points)
    #     mesh = p2m.points_and_tris_to_mesh_old(points, tris)
    #     facets = p2m.mesh_to_facets(mesh)
    #     return MirrorSurface(
    #         name, design_focal_length, points, tris, mesh, facets, uncertainties=True
    #     )

    # def from_csv(
    #     self, name: str, design_focal_length: float, file_path: str
    # ) -> MirrorSurface:
    #     """
    #     Loads a pointcloud data file from a csv.
    #     Pre-processes it to create mesh data as well.
    #     """
    #     p2m = PointsToMeshConverter()
    #     points = self.load_csv_points(file_path)
    #     tris = p2m.points_to_tris_old(points)
    #     mesh = p2m.points_and_tris_to_mesh_old(points, tris)
    #     facets = p2m.mesh_to_facets(mesh)
    #     return MirrorSurface(
    #         name, design_focal_length, points, tris, mesh, facets, uncertainties=True
    #     )

    # def load_csv_points(self, file_path: str) -> pd.DataFrame:
    #     """
    #     Load csv
    #     Doesn't have uncertainty and can't assume it's been pre-orientated.
    #     """
    #     points = pd.read_csv(
    #         file_path, delimiter=",", header=None, names=["x", "y", "z"]
    #     )
    #     points = self.scale_mm_to_m(points)
    #     return points
