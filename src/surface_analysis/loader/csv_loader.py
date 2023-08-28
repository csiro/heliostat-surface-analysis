import pandas as pd
import numpy as np

from surface_analysis.loader.loader import Loader


class CSV_Loader(Loader):
    def load_points(self, file_path: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Load a point cloud x, y, z as Nx1 arrays
        """
        points = self.load_csv_points(file_path)
        return (
            points["x"].to_numpy().reshape(-1, 1),
            points["y"].to_numpy().reshape(-1, 1),
            points["z"].to_numpy().reshape(-1, 1),
        )

    def load_csv_points(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(
            file_path,
            names=["x", "y", "z"],
        )
