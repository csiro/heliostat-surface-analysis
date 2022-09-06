from typing import Callable

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize

from surface_analysis.mirror_surface_plotter import MirrorSurface


class MirrorPlotter:
    @staticmethod
    def plot_mirror_3d(mirror: MirrorSurface, z_lim: list[float] = None) -> None:
        """
        Plot a triangulated surface.
        Triangulation is just done with x and y so need to include points for z data.
        """
        points = mirror.points
        tris = mirror.tris
        facets = mirror.facets

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

        p3dc = ax.plot_trisurf(
            points["x"],
            points["y"],
            points["z"],
            triangles=tris.simplices,
        )

        # Set up colours
        norm = Normalize()
        cmap = cm.get_cmap("plasma")
        colors = cmap(norm(facets["z"]))
        p3dc.set_fc(colors)
        fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm), shrink=0.5)
        fig.tight_layout()

        if z_lim is not None:
            ax.set_zlim(z_lim)

        plt.show()

    @staticmethod
    def plot_mirror_front_with_text(mirror: MirrorSurface) -> None:
        """
        Plot mirror viewed from the x direction with text of each point.
        """
        points = mirror.points

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.scatter(points["y"], points["z"])

        for _, row in points.iterrows():
            ax.text(row["y"], row["z"], str(int(row.name)+1))

        plt.show()

    @staticmethod
    def plot_mirror_and_fit(mirror: MirrorSurface, fit: Callable[[float, float], float]) -> None:
        """
        Plot a triangulated surface.
        Triangulation is just done with x and y so need to include points for z data.
        """
        points = mirror.points
        tris = mirror.tris
        facets = mirror.facets

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")
        p3dc = ax.plot_trisurf(
            points["x"],
            points["y"],
            points["z"],
            triangles=tris.simplices,
        )

        ax.scatter(
            points["x"],
            points["y"],
            points.apply(lambda row: fit(row["x"], row["y"]), axis=1)
        )

        # Set up colours
        norm = Normalize()
        cmap = cm.get_cmap("plasma")
        colors = cmap(norm(facets["z"]))
        p3dc.set_fc(colors)
        fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm), shrink=0.5)

        fig.tight_layout()
        plt.show()

    @staticmethod
    def plot_2d_func(func: Callable[[np.ndarray], float], points: np.ndarray, z_lim: list[float] = None) -> None:
        """
        func must operate on 1x2 array.
        points must be Nx2 array.
        """
        output = np.apply_along_axis(func, 1, points)
        MirrorPlotter.plot_2d(points, output, z_lim=z_lim)

    @staticmethod
    def plot_2d_func_diff(
        func0: Callable[[np.ndarray], float],
        func1: Callable[[np.ndarray], float],
        points: np.ndarray,
        z_lim: list[float] = None,
    ) -> None:
        """
        func must operate on 1x2 array.
        points must be Nx2 array.
        """
        output0 = np.apply_along_axis(func0, 1, points)
        output1 = np.apply_along_axis(func1, 1, points)
        MirrorPlotter.plot_2d(points, output1 - output0, z_lim=z_lim)


    @staticmethod
    def plot_2d(xy: np.ndarray, z: np.ndarray, z_lim: list[float] = None) -> None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(
            xy[:, 0],
            xy[:, 1],
            z,   
        )
        if z_lim is not None:
            ax.set_zlim(z_lim)

        plt.show()
