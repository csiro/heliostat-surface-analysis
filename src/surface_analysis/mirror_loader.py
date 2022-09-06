import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

from surface_analysis.mirror_surface import MirrorSurface
from surface_analysis.points_to_mesh_converter import PointsToMeshConverter as p2m


class MirrorLoader:
    @staticmethod
    def from_leica(
        name: str, design_focal_length: float, file_path: str
    ) -> MirrorSurface:
        """
        Loads a pointcloud data file from the Leica Absolute Tracker.
        Pre-processes it to create mesh data as well.
        """
        points = MirrorLoader.load_leica_points(file_path)
        tris = p2m.points_to_tris(points)
        mesh = p2m.points_and_tris_to_mesh(points, tris)
        facets = p2m.mesh_to_facets(mesh)
        return MirrorSurface(
            name, design_focal_length, points, tris, mesh, facets, uncertainties=True
        )

    @staticmethod
    def load_leica_points(file_path: str) -> pd.DataFrame:
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
        points = MirrorLoader.cleanup_leica_columns(points)
        points = MirrorLoader.scale_mm_to_m(points)
        return MirrorLoader.centre_points(points)

    @staticmethod
    def cleanup_leica_columns(points: pd.DataFrame) -> pd.DataFrame:
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

    @staticmethod
    def scale_mm_to_m(points: pd.DataFrame) -> pd.DataFrame:
        points = points.copy()
        points /= 1000
        return points

    @staticmethod
    def centre_points(points: pd.DataFrame) -> pd.DataFrame:
        points = points.copy()
        points["x"] -= points["x"].mean()
        points["y"] -= points["y"].mean()
        points["z"] -= points["z"].mean()
        return points

    @staticmethod
    def from_csv(
        name: str, design_focal_length: float, file_path: str
    ) -> MirrorSurface:
        """
        Loads a pointcloud data file from a csv.
        Pre-processes it to create mesh data as well.
        """
        points = MirrorLoader.load_csv_points(file_path)
        tris = p2m.points_to_tris(points)
        mesh = p2m.points_and_tris_to_mesh(points, tris)
        facets = p2m.mesh_to_facets(mesh)
        return MirrorSurface(
            name, design_focal_length, points, tris, mesh, facets, uncertainties=True
        )

    @staticmethod
    def load_csv_points(file_path: str) -> pd.DataFrame:
        """
        Load csv 
        Doesn't have uncertainty and can't assume it's been pre-orientated.
        """
        points = pd.read_csv(
            file_path,
            delimiter=",",
            header=None,
            names=["x", "y", "z"]
        )
        points = MirrorLoader.scale_mm_to_m(points)
        return points

 
    @staticmethod
    def rotate_points(points: pd.DataFrame) -> pd.DataFrame:
        points = points.copy()
        positions = np.array(points[["x", "y", "z"]])

        pca = PCA(n_components=3)
        pca.fit(positions)

        rotation = np.array(pca.components_).T
        new_positions = rotation.dot(positions.T).T

        points["x"] = new_positions[:, 0]
        points["y"] = new_positions[:, 1]
        points["z"] = new_positions[:, 2]

        return points
