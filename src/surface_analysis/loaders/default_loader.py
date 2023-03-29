import pandas as pd
import numpy as np

from surface_analysis.loaders.loader import Loader


class DefaultLoader(Loader):
    def load_points(self, file_path: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Load a point cloud x, y, z as Nx1 arrays
        """
        points = self.tab_delim_points(file_path)
        return (
            points["x"].to_numpy().reshape(-1, 1),
            points["y"].to_numpy().reshape(-1, 1),
            points["z"].to_numpy().reshape(-1, 1),
        )

    def whitespace_delim_points(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(
            file_path,
            delim_whitespace=True,
            names=["x", "y", "z"],
        )
