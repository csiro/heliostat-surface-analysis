import math

import numpy as np
import scipy
from scipy.spatial import Delaunay
from sklearn.decomposition import PCA
from stl import mesh
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import basinhopping


class MirrorSurface:
    def __init__(self, mirror_name: str, design_focal_length: float, file_path: str):
        self.mirror_name = mirror_name
        self.design_focal_length = design_focal_length
        self.file_path = file_path
        self.points = self.load_points(file_path)
        self.mesh = self.create_mesh(self.points)
        self.facets = self.create_facets(self.mesh)

    def load_points(self, file_path: str) -> pd.DataFrame:
        points = pd.read_csv(
            file_path,
            skiprows=7,
            delimiter=",  ",
            header=None,
            engine="python",
        )
        points = self.cleanup_columns(points)
        return self.centre_and_rotate_points(points)

    def cleanup_columns(self, points):
        points = points.copy()
        columns_to_drop = list(range(4, 6)) + list(range(9, len(points.columns)))
        points.drop(
            points.columns[columns_to_drop],
            axis=1,
            inplace=True,
        )
        points.columns = [
            "index",
            "x",
            "y",
            "z",
            "del_x",
            "del_y",
            "del_z",
        ]
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

    def create_mesh(self, data: pd.DataFrame) -> mesh.Mesh:
        xy_points = data[["x", "y"]].to_numpy()
        xyz_points = data[["x", "y", "z"]].to_numpy()
        triangles = Delaunay(xy_points)

        surface_mesh = mesh.Mesh(
            np.zeros(triangles.simplices.shape[0], dtype=mesh.Mesh.dtype)
        )
        for i, simplex in enumerate(triangles.simplices):
            for j in range(3):
                surface_mesh.vectors[i][j] = xyz_points[simplex[j], :]

        surface_mesh.update_normals()

        return surface_mesh

    def create_facets(self, mesh_data: mesh.Mesh) -> pd.DataFrame:
        facets = pd.DataFrame(
            data=mesh_data.points,
            dtype=float,
            columns=["x1", "y1", "z1", "x2", "y2", "z2", "x3", "y3", "z3"],
        )
        facets["x"] = (facets["x1"] + facets["x2"] + facets["x3"]) / 3.0
        facets["y"] = (facets["y1"] + facets["y2"] + facets["y3"]) / 3.0
        facets["z"] = (facets["z1"] + facets["z2"] + facets["z3"]) / 3.0
        facets["r"] = np.sqrt(facets["x"] ** 2 + facets["y"] ** 2)

        normals = pd.DataFrame(
            mesh_data.normals,
            dtype=float,
            columns=["x", "y", "z"],
        )

        normals["mag"] = np.linalg.norm(normals, axis=1)
        facets["normal"] = normals.apply(
            lambda row: [row["x"], row["y"], row["z"]] / row["mag"],
            axis=1,
        )

        return facets

    def fit_circular_paraboloid(self, points: pd.DataFrame) -> float:
        """
        Fit a circular paraboloid to the data.
        z = ax^2 + ay^2
        Return the a coefficient
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        Z = x

        A = np.array([])

        r = np.linalg.norm(
            points[["x", "y"]],
            axis=1,
        )
        z = np.array(points["z"])
        p = np.polyfit(r, z, 2)
        poly = np.poly1d(p)
        print(poly)
        return poly

    def make_ideal_data(self):
        self.surface_mesh_data["design_z"] = \
            (self.surface_mesh_data["x"] ** 2 + self.surface_mesh_data["y"] ** 2) / (4 * self.design_focal_length)
        self.surface_mesh_data["bestfit_z"] = \
            (self.surface_mesh_data["x"] ** 2 + self.surface_mesh_data["y"] ** 2) * self.p[0] + \
            (self.surface_mesh_data["x"] + self.surface_mesh_data["y"]) * self.p[1]

        design_normals = []
        bestfit_normals = []
        for _, row in self.surface_mesh_data.iterrows():
            design_normal = self.slope_of_parabloid_at_point(
                row["x"], row["y"], 1 / (4.0 * self.design_focal_length), 0
            )
            bestfit_normal = self.slope_of_parabloid_at_point(
                row["x"], row["y"], self.p[0], self.p[1]
            )
            design_normals.append(design_normal)
            bestfit_normals.append(bestfit_normal)

        self.surface_mesh_data["design_normals"] = design_normals
        self.surface_mesh_data["bestfit_normals"] = bestfit_normals

    def get_mesh_normals(self):
        self.surface_mesh_data["design_z"] = (
            self.surface_mesh_data["x"] ** 2 + self.surface_mesh_data["y"] ** 2
        ) / (4 * self.design_focal_length)
        self.surface_mesh_data["bestfit_z"] = (
            self.surface_mesh_data["x"] ** 2 + self.surface_mesh_data["y"] ** 2
        ) * self.p[0] + 0 * (
            self.surface_mesh_data["x"] + self.surface_mesh_data["y"]
        ) * self.p[
            1
        ]
        design_normals = []
        bestfit_normals = []
        for idx, row in self.surface_mesh_data.iterrows():
            design_normal = self.slope_of_parabloid_at_point(
                row["x"], row["y"], 1 / (4 * self.design_focal_length), 0
            )
            bestfit_normal = self.slope_of_parabloid_at_point(
                row["x"], row["y"], self.p[0], 0 * self.p[1]
            )
            design_normals.append(design_normal)
            bestfit_normals.append(bestfit_normal)

        self.surface_mesh_data["design_normals"] = design_normals
        self.surface_mesh_data["bestfit_normals"] = bestfit_normals

    def make_error_data(self):
        errors = []
        errors_bestfit = []
        for _, row in self.surface_mesh_data.iterrows():
            error = self.get_angle_between_2_vector(
                row["design_normals"], row["normal"]
            )
            error_bestfit = self.get_angle_between_2_vector(
                row["bestfit_normals"], row["normal"]
            )
            errors.append(error)
            errors_bestfit.append(error_bestfit)
        self.surface_mesh_data["design_slope_error"] = errors
        self.surface_mesh_data["bestfit_slope_error"] = errors_bestfit

        mean_design = (
            (self.surface_mesh_data["design_slope_error"] ** 2).mean()
        ) ** 0.5
        mean_best = ((self.surface_mesh_data["bestfit_slope_error"] ** 2).mean()) ** 0.5

        self.sigma_best = np.sqrt(2 / np.pi) * mean_best
        self.sigma_design = np.sqrt(2 / np.pi) * mean_design

    def make_histogram_data(self):
        a = self.surface_mesh_data["design_slope_error"]
        count, bins, ignored = plt.hist(a, 100, normed=True)
        mu, sigma = 0.0, self.sigma_design
        plt.plot(
            bins,
            bins / (sigma**2) * np.exp(-((bins) ** 2) / (2 * sigma**2)),
            linewidth=2,
            color="r",
        )
        plt.show()

        b = self.surface_mesh_data["bestfit_slope_error"]
        count, bins, ignored = plt.hist(b, 100, normed=True)
        mu, sigma = 0.0, self.sigma_best
        plt.plot(
            bins,
            (bins / (sigma**2)) * np.exp(-((bins) ** 2) / (2 * sigma**2)),
            linewidth=2,
            color="r",
        )
        plt.show()

    def slope_of_parabloid_at_point(self, x, y, p0, p1):
        gradient_x = 2 * x * p0 + p1
        gradient_y = 2 * y * p0 + p1
        Tx = self.unit_vector([1, 0, gradient_x])
        Ty = self.unit_vector([0, 1, gradient_y])
        return np.cross(Tx, Ty)

    def unit_vector(self, data):
        data = np.array(data, dtype=np.float64, copy=True)
        return math.sqrt(np.dot(data, data))

    def get_angle_between_2_vector(self, u, v):
        inner_product = u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
        scalar_1 = math.sqrt(u[0] ** 2 + u[1] ** 2 + u[2] ** 2)
        scalar_2 = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)

        cos_theta = inner_product / (scalar_1 * scalar_2)
        return math.acos(cos_theta)

    def plot_radial(self):
        df = self.point_data
        df2 = self.surface_mesh_data
        plt.scatter(df["r"], df["z"], marker=".")
        plt.scatter(df2["r"], df2["z"], marker=".")
        plt.plot(df2["r"], df2["design_z"])
        plt.plot(df2["r"], df2["best_fit"])
        plt.ylabel("z")
        plt.xlabel("r")
        plt.savefig("{0}_plot_r_y.png".format(self.mirror_name))
        plt.clf()
        plt.cla()

    def plot_slope(self):
        df = self.surface_mesh_data
        plt.scatter(df["r"], df["best_fit_slope_r"], marker=".")
        plt.plot(df["r"], df["design_slope_r"])
        plt.ylabel("dz/dr")
        plt.xlabel("r")
        plt.savefig("{0}_plot_dzdr.png".format(self.mirror_name))
        plt.clf()
        plt.cla()

    def plot_slope_surface(self):
        plt.cla()
        plt.clf()
        df = self.surface_mesh_data
        x = df["x"]
        y = df["y"]
        z = df["design_slope_error"]

        # Set up a regular grid of interpolation points
        xi, yi = np.linspace(x.min(), x.max(), 300), np.linspace(y.min(), y.max(), 300)
        xi, yi = np.meshgrid(xi, yi)

        # Interpolate; there's also method='cubic' for 2-D data such as here
        zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method="cubic")

        plt.imshow(
            zi,
            vmin=z.min(),
            vmax=z.max(),
            origin="lower",
            extent=[x.min(), x.max(), y.min(), y.max()],
            cmap="hot",
        )
        plt.colorbar()
        plt.savefig(
            "{0}_plot_design_slope_{1}.png".format(
                self.mirror_name, self.design_focal_length
            )
        )
        plt.clf()
        plt.cla()

    def fit_curve_to_radial(self):
        r = np.array(self.surface_mesh_data["r"])
        z = np.array(self.surface_mesh_data["z"])
        p = np.polyfit(r, z, 2)
        poly = np.poly1d(p)
        print(p)
        self.p = p
        self.surface_mesh_data["best_fit"] = poly(self.surface_mesh_data["r"])
        self.surface_mesh_data["best_fit_slope_r"] = (
            2 * p[0] * self.surface_mesh_data["r"] + p[1]
        )
        self.surface_mesh_data["design_slope_r"] = (
            2 * self.surface_mesh_data["r"] / (4 * self.design_focal_length)
        )

    def bivariatefit(self):
        df2 = self.point_data
        x = df2["x"]
        y = df2["y"]
        z = df2["z"]

        plt.cla()
        plt.clf()
        plt.scatter(x, y)
        plt.savefig("{0}_plot_xy_points.png".format(self.mirror_name))

        # Set up a regular grid of interpolation points
        print((x.max() - x.min()) * (y.max() - y.min()))
        print(2.25 * 2.25)
        print((x.max() - x.min()) * (y.max() - y.min()) / (2.25 * 2.25))
        xi, yi = np.linspace(x.min(), x.max(), 300), np.linspace(y.min(), y.max(), 300)
        xi, yi = np.meshgrid(xi, yi)
        tck = scipy.interpolate.SmoothBivariateSpline(
            self.point_data["x"], self.point_data["y"], self.point_data["z"]
        )
        zi = tck.ev(xi, yi)
        plt.cla()
        plt.clf()
        plt.imshow(
            zi,
            vmin=z.min(),
            vmax=z.max(),
            origin="lower",
            extent=[x.min(), x.max(), y.min(), y.max()],
            cmap="hot",
        )
        plt.colorbar()
        plt.savefig("{0}_plot_xyz_biv_fit.png".format(self.mirror_name))

        plt.cla()
        plt.clf()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_wireframe(xi, yi, zi, rstride=10, cstride=10)
        plt.savefig("{0}_plot_xyz_wireframe.png".format(self.mirror_name))

        plt.cla()
        plt.clf()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(
            xi,
            yi,
            zi,
            rstride=5,
            cstride=5,
            cmap=cm.coolwarm,
            linewidth=0,
        )
        plt.savefig("{0}_plot_xyz_3d.png".format(self.mirror_name))

    def fitbyz(self, vars):
        df2 = self.surface_mesh_data
        x = df2["x"]
        y = df2["y"]
        z = df2["z"]

        a = vars[0]
        b = vars[1]
        c = vars[2]
        d = vars[3]
        e = vars[4]
        f = vars[5]
        g = vars[6]
        h = vars[7]
        z2 = (
            a * (x**2) * (y**2)
            + b * (x**2) * y
            + c * (x**2)
            + d * x * (y**2)
            + e * x * y
            + f * x
            + g * (y**2)
            + h * y
        )

        error = (((z - z2) ** 2).mean()) ** 0.5
        return error

    def plot_est_func(self, vars):
        df2 = self.surface_mesh_data
        x = df2["x"]
        y = df2["y"]
        z = df2["z"]

        a = vars[0]
        b = vars[1]
        c = vars[2]
        d = vars[3]
        e = vars[4]
        f = vars[5]
        g = vars[6]
        h = vars[7]

        zideal = (1 / (4 * self.design_focal_length)) * x**2 + (
            1 / (4 * self.design_focal_length)
        ) * y**2
        z0 = a * x**2 + b * y**2
        z1 = z0 - zideal
        self.plot_int(x, y, z1, "focal_length_error")
        z2 = c * x + d * y
        self.plot_int(x, y, z2, "rotated_error")
        z3 = e * x * y
        self.plot_int(x, y, z3, "twist_error")
        z4 = (g * x**2 + h * y**2) ** 0.5
        self.plot_int(x, y, z4, "error_conical")
        z5 = z1 + z2 + z3 + z4 + f - z
        self.plot_int(x, y, z5, "residuals")

    def plot_int(self, x, y, z, label):
        plt.clf()
        plt.cla()
        xi = np.linspace(x.min(), x.max(), 800)
        yi = np.linspace(y.min(), y.max(), 800)
        xi, yi = np.meshgrid(xi, yi)

        # Interpolate; there's also method='cubic' for 2-D data such as here
        zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method="cubic")

        plt.imshow(
            zi,
            vmin=z.min(),
            vmax=z.max(),
            origin="lower",
            extent=[x.min(), x.max(), y.min(), y.max()],
            cmap="hot",
        )
        plt.colorbar()
        plt.savefig("{0}_plot_xyz_{1}.png".format(self.mirror_name, label))

    def find_fit(self):
        # the starting point
        x0 = np.array(
            [
                1.0 / (3.0 * self.design_focal_length),
                1.0 / (3.0 * self.design_focal_length),
                -0.0001,
                -0.0001,
                -0.0001,
                -0.1,
                -0.0001,
                -0.0001,
            ]
        )
        self.fitbyz(x0)

        # the bounds
        xmin = [
            1.0 / (self.design_focal_length * 4 * 2),
            1.0 / (self.design_focal_length * 4 * 2),
            -2.0,
            -2.0,
            -2.0,
            -0.2,
            0,
            0,
        ]
        xmax = [
            1.0 / (self.design_focal_length * 4 / 2),
            1.0 / (self.design_focal_length * 4 / 2),
            2.0,
            2.0,
            2.0,
            0.2,
            0.2,
            0.2,
        ]

        # rewrite the bounds in the way required by L-BFGS-B
        bounds = [(low, high) for low, high in zip(xmin, xmax)]

        # use method L-BFGS-B because the problem is smooth and bounded
        minimizer_kwargs = dict(method="L-BFGS-B", bounds=bounds)
        res = basinhopping(self.fitbyz, x0, minimizer_kwargs=minimizer_kwargs)

        print(res)
        params = res.x
        print(1 / (4 * params[0]), 1 / (4 * params[1]))
        self.plot_est_func(params)
        return params
