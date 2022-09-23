import os
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.figure import Figure

from surface_analysis.points_to_mesh_converter import (
    points_to_tris, points_and_tris_to_mesh, mesh_to_facets
)


class Plotter:
    def __init__(
        self,
        z_lim: list[float] = None,
    ) -> None:
        self.z_lim = z_lim

    def plot_points(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ):
        fig = plt.figure()
        self.add_points_subplot(fig, 111, x, y, z)
        plt.show()

    def plot_points_pair(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z0: np.ndarray,
        z1: np.ndarray,
    ):
        fig = plt.figure()
        self.add_points_subplot(fig, 121, x, y, z0)
        self.add_points_subplot(fig, 122, x, y, z1)
        plt.show()

    def plot_points_as_surface(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> None:
        fig = plt.figure()
        self.add_points_as_surface_subplot(fig, 111, x, y, z)
        plt.show()

    def plot_points_as_surface_pair(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z0: np.ndarray,
        z1: np.ndarray,
    ) -> None:
        fig = plt.figure()
        self.add_points_as_surface_subplot(fig, 121, x, y, z0)
        self.add_points_as_surface_subplot(fig, 122, x, y, z1)
        plt.show()

    def plot_points_as_surface_four(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z0: np.ndarray,
        z1: np.ndarray,
        z2: np.ndarray,
        z3: np.ndarray,
    ) -> None:
        fig = plt.figure()
        self.add_points_as_surface_subplot(fig, 221, x, y, z0)
        self.add_points_as_surface_subplot(fig, 222, x, y, z1)
        self.add_points_as_surface_subplot(fig, 223, x, y, z2)
        self.add_points_as_surface_subplot(fig, 224, x, y, z3)
        plt.show()

    def initial_verification_plots(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        output_dir: str,
    ):
        fig = plt.figure()
        self.add_points_subplot(fig, 111, x, y, z)
        plt.savefig(os.path.join(output_dir, "3d_points"))

        fig = plt.figure()
        self.add_points_as_surface_subplot(fig, 111, x, y, z)
        plt.savefig(os.path.join(output_dir, "3d_surface"))

        fig = plt.figure()
        self.add_points_with_text_subplot(fig, 111, x, y, z)
        plt.savefig(os.path.join(output_dir, "points_with_text"))

    def fit_verification_plots(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        output_dir: str,
        function_name: str,
    ) -> None:
        fig = plt.figure()
        self.add_points_subplot(fig, 111, x, y, z)
        plt.savefig(os.path.join(output_dir, f"{function_name}_3d_points"))

        fig = plt.figure()
        self.add_points_as_surface_subplot(fig, 111, x, y, z)
        plt.savefig(os.path.join(output_dir, f"{function_name}_3d_surface"))

    def slope_verification_plots(
        self,
        values: np.ndarray,
        output_dir: str,
        function_name: str,
        bins: int = 100,
    ) -> None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(
            values,
            bins=bins,
        )
        plt.savefig(os.path.join(output_dir, f"{function_name}_slope_hist"))

    def plot_hist(
        self,
        values: np.ndarray,
        bins: int = 100,
    ) -> None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(
            values,
            bins=bins,
        )
        ax.set_xlabel("Surface normal deviation (radian)")
        ax.set_ylabel("Frequency (counts per bin)")
        ax.set_xlim((0, 0.01))
        plt.show()

    def plot_hist_and_curve(
        self,
        values: np.ndarray,
        sigma: float,
        bin_count: int = 100,
    ) -> None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        count, bins, ignored = ax.hist(
            values,
            bins=bin_count,
            density=True,
        )
        plt.plot(
            bins,
            bins / (sigma**2) * np.exp(-1 * (bins) ** 2 / (2 * sigma**2)),
            color="r",
        )
        plt.show()

    def add_points_subplot(
        self,
        fig: Figure,
        subplot_number: int,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> None:
        ax = fig.add_subplot(subplot_number, projection="3d")
        ax.scatter(x, y, z)
        ax.set_zlim(self.z_lim)

    def add_points_as_surface_subplot(
        self,
        fig: plt.Figure,
        subplot_number: int,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> None:
        tris = points_to_tris(x, y)
        mesh = points_and_tris_to_mesh(x, y, z, tris)
        facets = mesh_to_facets(mesh)

        ax = fig.add_subplot(subplot_number, projection="3d")
        ax.set_xlabel("\nX (m)")
        ax.set_ylabel("\nY (m)")
        ax.set_zlabel("\nZ (m)")
        p3dc = ax.plot_trisurf(
            x.reshape((-1,)),
            y.reshape((-1,)),
            z.reshape((-1,)),
            triangles=tris.simplices,
        )

        # Set up colours
        norm = Normalize()
        cmap = cm.get_cmap("plasma")
        colors = cmap(norm(facets["z"]))
        p3dc.set_fc(colors)
        # cbar = fig.colorbar(
        #     cm.ScalarMappable(cmap=cmap, norm=norm),
        #     shrink=0.4,
        #     pad=0,
        #     orientation="horizontal",
        # )
        # cbar.set_label("Z-axis position (m)")
        # fig.tight_layout()
        ax.set_zlim(self.z_lim)
        ax.set_box_aspect((1,1,0.5))

    def add_points_with_text_subplot(
        self,
        fig: plt.Figure,
        subplot_number: int,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> None:
        ax = fig.add_subplot(subplot_number)
        ax.scatter(x, z)
        for i in range(len(x)):
            ax.text(x[i], z[i], str(i))

    def plot_points_top_view(
        self,
        x: np.ndarray,
        y: np.ndarray,
    ) -> None:
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.plot(x, y, markersize=5)
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        fig.show()

    def plot_3d_func_diff(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z_func0: Callable[[np.ndarray, np.ndarray], np.ndarray],
        z_func1: Callable[[np.ndarray, np.ndarray], np.ndarray],
    ) -> None:
        z0 = z_func0(x, y)
        z1 = z_func1(x, y)
        ax = self.plot_points(
            x,
            y,
            z1 - z0,
        )

    def plot_3d_func(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    ) -> None:
        z = z_func(x, y)
        ax = self.plot_points(
            x,
            y,
            z,
        )
        ax.set_zlim(self.z_lim)

    # def plot_mirror_3d(
    #     self,
    #     mirror: MirrorSurface,
    # ) -> None:
    #     """
    #     Plot a triangulated surface.
    #     Triangulation is just done with x and y so need to include points for z data.
    #     """
    #     points = mirror.points
    #     tris = mirror.tris
    #     facets = mirror.facets

    #     ax = self.fig.add_subplot(1, 2, 1, projection="3d")
    #     ax.set_xlabel("x (m)")
    #     ax.set_ylabel("y (m)")
    #     ax.set_zlabel("z (m)")

    #     p3dc = ax.plot_trisurf(
    #         points["x"],
    #         points["y"],
    #         points["z"],
    #         triangles=tris.simplices,
    #     )

    #     # Set up colours
    #     norm = Normalize()
    #     cmap = cm.get_cmap("plasma")
    #     colors = cmap(norm(facets["z"]))
    #     p3dc.set_fc(colors)
    #     cbar = self.fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm), shrink=0.5)
    #     cbar.set_label("z (mm)")
    #     self.fig.tight_layout()
    #     ax.set_zlim(self.z_lim)

    # def plot_mirror_and_3d_func(
    #     self,
    #     mirror: MirrorSurface,
    #     z_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    # ) -> None:
    #     """
    #     Plot a triangulated surface.
    #     Triangulation is just done with x and y so need to include points for z data.
    #     """
    #     points = mirror.points
    #     tris = mirror.tris
    #     facets = mirror.facets

    #     x = points["x"].to_numpy().reshape(-1, 1)
    #     y = points["y"].to_numpy().reshape(-1, 1)
    #     facet_z = facets["z"].to_numpy().reshape(-1, 1)

    #     ax = self.fig.add_subplot(111, projection="3d")
    #     p3dc = ax.plot_trisurf(
    #         points["x"],
    #         points["y"],
    #         points["z"],
    #         triangles=tris.simplices,
    #     )
    #     ax.scatter(
    #         x,
    #         y,
    #         z_func(x, y),
    #     )

    #     # Set up colours
    #     norm = Normalize()
    #     cmap = cm.get_cmap("plasma")
    #     colors = cmap(norm(facet_z))
    #     p3dc.set_fc(colors)
    #     self.fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm), shrink=0.5)
    #     self.fig.tight_layout()

    # def plot_mirror_and_3d_func_diff(
    #     self,
    #     mirror: MirrorSurface,
    #     z_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    # ) -> None:
    #     """
    #     Plot a triangulated surface.
    #     Triangulation is just done with x and y so need to include points for z data.
    #     """
    #     points = mirror.points
    #     tris = mirror.tris
    #     facets = mirror.facets

    #     x = points["x"].to_numpy().reshape(-1, 1)
    #     y = points["y"].to_numpy().reshape(-1, 1)
    #     z = points["z"].to_numpy().reshape(-1, 1)
    #     facet_x = facets["x"].to_numpy().reshape(-1, 1)
    #     facet_y = facets["y"].to_numpy().reshape(-1, 1)
    #     facet_z = facets["z"].to_numpy().reshape(-1, 1)

    #     ax = self.fig.add_subplot(111, projection="3d")
    #     p3dc = ax.plot_trisurf(
    #         points["x"],
    #         points["y"],
    #         (z - z_func(x, y)).reshape((-1,)),
    #         triangles=tris.simplices,
    #     )

    #     # Set up colours
    #     norm = Normalize()
    #     cmap = cm.get_cmap("plasma")
    #     colors = cmap(norm(facet_z - z_func(facet_x, facet_y)))
    #     p3dc.set_fc(colors)
    #     self.fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm), shrink=0.5)
    #     self.fig.tight_layout()

    # def plot_mirror_front_with_text(
    #     self,
    #     mirror: MirrorSurface,
    # ) -> None:
    #     """
    #     Plot mirror viewed from the x direction with text of each point.
    #     """
    #     points = mirror.points

    #     fig, ax = plt.subplots(figsize=(10, 10))
    #     ax.scatter(points["y"], points["z"])

    #     for _, row in points.iterrows():
    #         ax.text(row["y"], row["z"], str(int(row.name) + 1))
