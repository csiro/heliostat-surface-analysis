import numpy as np
import matplotlib.pyplot as plt

from typing import Union, Optional, cast

from surface_analysis.preprocessor.basic_preprocessor import BasicPreprocessor


class KnownSizePreprocessor(BasicPreprocessor):
    def __init__(
        self,
        params: Optional[dict[str, Union[str, float]]]
    ):
        params = cast(dict[str, Union[str, float]], params)
        width = float(params["width"])
        height = float(params["height"])
        self.width = width
        self.height = height

    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        x, y, z = super().preprocess_points(raw_x, raw_y, raw_z)
        return self.rotate_xy_plane(x, y, z)

    def rotate_xy_plane(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        points = np.hstack((raw_x, raw_y, raw_z)).T

        best_theta = 0
        best_area = 999
        steps = 200
        for theta in np.arange(0, np.pi, np.pi / steps):
            rot = np.array(
                [[np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]]
            )
            rotated_points = rot @ points

            max_x = np.max(np.absolute(rotated_points[0,:]))
            max_y = np.max(np.absolute(rotated_points[1,:]))

            if max_x * max_y < best_area:
                best_area = max_x * max_y
                best_theta = theta

        rot = np.array(
            [[np.cos(best_theta), -np.sin(best_theta), 0],
            [np.sin(best_theta), np.cos(best_theta), 0],
            [0, 0, 1]]
        )
        rotated_points = rot @ points

        ###
        fig, ax = plt.subplots()
        ax.scatter(rotated_points[0,:], rotated_points[1,:])
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        # square_x = [-max_x, max_x, max_x, -max_x, -max_x]
        # square_y = [-max_y, -max_y, max_y, max_y, -max_y]

        # ax.plot(square_x, square_y)

        plt.show()
        ###

        return raw_x, raw_y, raw_z
