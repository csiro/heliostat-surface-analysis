import numpy as np

from surface_analysis.loader.default_loader import DefaultLoader


class ScalingLoader(DefaultLoader):
    def load_points(self, file_path: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        x, y, z = super().load_points(file_path)
        return (
            x / 1000,
            y / 1000,
            z / 1000,
        )
