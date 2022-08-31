import pandas as pd

from mirror_surface import MirrorSurface


class MirrorLoader:
    def from_leica(
        self, mirror_id: str, design_focal_length: float, file_path: str
    ) -> MirrorSurface:
        points = MirrorLoader.load_leica_points(file_path)

    def load_leica_points(file_path: str) -> pd.DataFrame:
        """Loads a pointcloud data file from the Leica Absolute Tracker."""
        points = pd.read_csv(
            file_path,
            skiprows=7,
            delimiter=",  ",
            header=None,
            engine="python",
        )
        points = MirrorLoader.cleanup_leica_columns(points)
        points = MirrorLoader.scale_mm_to_m(points)
        return MirrorLoader.centre_and_rotate_points(points)

    def cleanup_leica_columns(self, points: pd.DataFrame) -> pd.DataFrame:
        """Label columns and drop the unnecessary ones."""
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

    def centre_and_rotate_points(self, points: pd.DataFrame) -> pd.DataFrame:
        points["x"] -= points["x"].mean()
        points["y"] -= points["y"].mean()
        points["z"] -= points["z"].mean()

        positions = np.array(points[["x", "y", "z"]], copy=True)
        uncertainties = np.array(points[["del_x", "del_y", "del_z"]], copy=True)

        pca = PCA(n_components=3)
        pca.fit(positions)

        rotation = np.array(pca.components_).T
        new_positions = rotation.dot(positions.T).T
        new_uncertainties = rotation.dot(uncertainties.T).T

        points["x"] = new_positions[:, 0]
        points["y"] = new_positions[:, 1]
        points["z"] = new_positions[:, 2]
        points["del_x"] = new_uncertainties[:, 0]
        points["del_y"] = new_uncertainties[:, 1]
        points["del_z"] = new_uncertainties[:, 2]

        return points
