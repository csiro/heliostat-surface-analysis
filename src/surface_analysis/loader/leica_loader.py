import pandas as pd
import numpy as np

from surface_analysis.loader.loader import Loader

import typing

class LeicaLoader(Loader):
    def load_points(self, file_path: str) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
