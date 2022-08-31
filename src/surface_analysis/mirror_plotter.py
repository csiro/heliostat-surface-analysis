from typing import Callable
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize

from surface_analysis.mirror_surface_plotter import MirrorSurface


class MirrorPlotter:
    @staticmethod
    def plot_mirror(mirror: MirrorSurface) -> None:
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
