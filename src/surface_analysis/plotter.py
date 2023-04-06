import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.figure import Figure
from matplotlib.cm import ScalarMappable
from cmcrameri import cm

from surface_analysis.points_to_mesh_converter import points_to_tris


class Plotter:
    def plot_points(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        output_dir: str,
        title: str,
        x_units: str,
        y_units: str,
        z_units: str,
    ) -> None:
        fig = plt.figure()
        self.add_points_subplot(
            fig,
            111,
            x,
            y,
            z,
            x_units,
            y_units,
            z_units,
        )
        plt.savefig(os.path.join(output_dir, f"{title}_points"), dpi=1200)

    # def plot_points_pair(
    #     self,
    #     x: np.ndarray,
    #     y: np.ndarray,
    #     z0: np.ndarray,
    #     z1: np.ndarray,
    #     output_dir: str,
    #     title: str,
    #     x_units: str,
    #     y_units: str,
    #     z_units: str,
    # ):
    #     fig = plt.figure()
    #     self.add_points_subplot(fig, 121, x, y, z0)
    #     self.add_points_subplot(fig, 122, x, y, z1)
    #     plt.savefig(os.path.join(output_dir, f"{title}_pair_points"), dpi=1200)

    def plot_points_as_surface(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        z_c: np.ndarray,
        output_dir: str,
        title: str,
        x_units: str,
        y_units: str,
        z_units: str,
        zero: bool = False,
    ) -> None:
        fig = plt.figure()
        self.add_points_as_surface_subplot(
            fig,
            111,
            x,
            y,
            z,
            z_c,
            x_units,
            y_units,
            z_units,
            zero=zero
        )
        plt.savefig(os.path.join(output_dir, f"{title}_surface"), dpi=1200)

    # def plot_points_as_surface_pair(
    #     self,
    #     x: np.ndarray,
    #     y: np.ndarray,
    #     z0: np.ndarray,
    #     z1: np.ndarray,
    #     output_dir: str,
    #     title: str,
    # ) -> None:
    #     fig = plt.figure()
    #     self.add_points_as_surface_subplot(fig, 121, x, y, z0)
    #     self.add_points_as_surface_subplot(fig, 122, x, y, z1)
    #     plt.savefig(os.path.join(output_dir, f"{title}_pair_surface"), dpi=1200)

    # def plot_points_as_surface_four(
    #     self,
    #     x: np.ndarray,
    #     y: np.ndarray,
    #     z0: np.ndarray,
    #     z1: np.ndarray,
    #     z2: np.ndarray,
    #     z3: np.ndarray,
    #     output_dir: str,
    #     title: str,
    # ) -> None:
    #     fig = plt.figure()
    #     self.add_points_as_surface_subplot(fig, 221, x, y, z0)
    #     self.add_points_as_surface_subplot(fig, 222, x, y, z1)
    #     self.add_points_as_surface_subplot(fig, 223, x, y, z2)
    #     self.add_points_as_surface_subplot(fig, 224, x, y, z3)
    #     plt.savefig(os.path.join(output_dir, f"{title}_four_surface"), dpi=1200)

    def plot_points_2d(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        output_dir: str,
        title: str,
        x_units: str,
        y_units: str,
        z_units: str,
        zero: bool = False,
    ) -> None:
        fig = plt.figure()
        self.add_points_2d_subplot(
            fig,
            111,
            x,
            y,
            z,
            x_units,
            y_units,
            z_units,
            zero=zero
        )
        plt.savefig(os.path.join(output_dir, f"{title}_points_2d"), dpi=1200)

    # def plot_points_with_indexes(
    #     self,
    #     x: np.ndarray,
    #     y: np.ndarray,
    #     z: np.ndarray,
    #     output_dir: str,
    #     title: str,
    # ) -> None:
    #     fig = plt.figure()
    #     self.add_points_with_text_subplot(fig, 111, x, y, z)
    #     plt.savefig(os.path.join(output_dir, f"{title}_indexes"), dpi=1200)

    def add_points_subplot(
        self,
        fig: Figure,
        subplot_number: int,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        x_units: str,
        y_units: str,
        z_units: str, 
    ) -> None:
        ax = fig.add_subplot(subplot_number, projection="3d")
        ax.scatter(x, y, z)
        ax.set_xlabel(x_units)
        ax.set_ylabel(y_units)
        ax.set_zlabel(z_units)

    def add_points_as_surface_subplot(
        self,
        fig: plt.Figure,
        subplot_number: int,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        z_c: np.ndarray,
        x_units: str,
        y_units: str,
        z_units: str,
        zero: bool = False,
    ) -> None:
        tris = points_to_tris(x, y)

        ax = fig.add_subplot(subplot_number, projection="3d")
        ax.set_xlabel(f"\nX ({x_units})")
        ax.set_ylabel(f"\nY ({y_units})")
        p3dc = ax.plot_trisurf(
            x.reshape((-1,)),
            y.reshape((-1,)),
            z.reshape((-1,)),
            triangles=tris.simplices,
        )

        # Set up colours
        if zero:
            max_value = max(max(z_c), abs(min(z_c)))
            norm = Normalize(-max_value, max_value)
            colors = cm.vik(norm(z_c))
            m = ScalarMappable(cmap=cm.vik, norm=norm)
        else:
            norm = Normalize()
            colors = cm.batlow(norm(z_c))
            m = ScalarMappable(cmap=cm.batlow, norm=norm)

        p3dc.set_fc(colors)
        m.set_array([])
        cbar = plt.colorbar(m, pad=0.1, label=z_units)
        # cbar.ax.set_ylabel(z_units, rotation=270)

        ax.set_box_aspect((1,1,0.5))
        ax.set_xlabel(x_units)
        ax.set_ylabel(y_units)

    def add_points_2d_subplot(
        self,
        fig: Figure,
        subplot_number: int,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        x_units: str,
        y_units: str,
        z_units: str,
        zero: bool = False,
    ) -> None:
        tris = points_to_tris(x, y)
        # mesh = points_and_tris_to_mesh(x, y, z, tris)
        # facets = mesh_to_facets(mesh)

        ax = fig.add_subplot(subplot_number)
        x = np.ravel(x)
        y = np.ravel(y)
        z = np.ravel(z)

        if zero:
            max_value = max(max(z), abs(min(z)))
            norm = Normalize(-max_value, max_value)
            tpc = ax.tripcolor(x, y, tris.simplices, facecolors=z, edgecolors='k', cmap=cm.vik, norm=norm)
        else:
            tpc = ax.tripcolor(x, y, tris.simplices, facecolors=z, edgecolors='k', cmap=cm.batlow)

        ax.set_xlabel(x_units)
        ax.set_ylabel(y_units)


        cbar = fig.colorbar(tpc, label=z_units)

    # def add_points_with_text_subplot(
    #     self,
    #     fig: plt.Figure,
    #     subplot_number: int,
    #     x: np.ndarray,
    #     y: np.ndarray,
    #     z: np.ndarray,
    # ) -> None:
    #     ax = fig.add_subplot(subplot_number)
    #     ax.scatter(x, z)
    #     for i in range(len(x)):
    #         ax.text(x[i], z[i], str(i))

    # def slope_verification_plots(
    #     self,
    #     values: np.ndarray,
    #     output_dir: str,
    #     function_name: str,
    #     bins: int = 100,
    # ) -> None:
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111)
    #     ax.hist(
    #         values,
    #         bins=bins,
    #     )
    #     plt.savefig(os.path.join(output_dir, f"{function_name}_slope_hist"))

    # def plot_hist(
    #     self,
    #     values: np.ndarray,
    #     bins: int = 100,
    # ) -> None:
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111)
    #     ax.hist(
    #         values,
    #         bins=bins,
    #     )
    #     ax.set_xlabel("Surface normal deviation (radian)")
    #     ax.set_ylabel("Frequency (counts per bin)")
    #     ax.set_xlim((0, 0.01))
    #     plt.show()

    # def plot_hist_and_curve(
    #     self,
    #     values: np.ndarray,
    #     sigma: float,
    #     bin_count: int = 100,
    # ) -> None:
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111)
    #     count, bins, ignored = ax.hist(
    #         values,
    #         bins=bin_count,
    #         density=True,
    #     )
    #     plt.plot(
    #         bins,
    #         bins / (sigma**2) * np.exp(-1 * (bins) ** 2 / (2 * sigma**2)),
    #         color="r",
    #     )
    #     plt.show()

    # def plot_points_top_view(
    #     self,
    #     x: np.ndarray,
    #     y: np.ndarray,
    # ) -> None:
    #     fig = plt.figure()
    #     ax = fig.add_subplot()
    #     ax.plot(x, y, markersize=5)
    #     ax.set_xlabel("X (m)")
    #     ax.set_ylabel("Y (m)")
    #     fig.show()
