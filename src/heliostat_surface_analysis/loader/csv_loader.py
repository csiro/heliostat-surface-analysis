import pandas as pd
import numpy as np
import typing

from heliostat_surface_analysis.loader.loader import Loader


class CSVLoader(Loader):
    def __init__(
        self,
        params: typing.Optional[typing.Dict[str, typing.Union[str, float]]]
    ):
        params = typing.cast(
            typing.Dict[str, typing.Union[str, float]],
            params or {}
        )

        units = str(params.get("units", "m"))

        if units == "mm":
            self.scale_factor = 1.0e-3
        elif units == "cm":
            self.scale_factor = 1.0e-2
        elif units == "m":
            self.scale_factor = 1.0
        else:
            raise RuntimeError(f"units {units} not recognised")

    def load_points(self, file_path: str) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Load a point cloud x, y, z as Nx1 arrays
        """
        points = self.load_csv_points(file_path)
        return (
            points["x"].to_numpy().reshape(-1, 1) * self.scale_factor,
            points["y"].to_numpy().reshape(-1, 1) * self.scale_factor,
            points["z"].to_numpy().reshape(-1, 1) * self.scale_factor,
        )

    def load_csv_points(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(
            file_path,
            names=["x", "y", "z"],
        )
