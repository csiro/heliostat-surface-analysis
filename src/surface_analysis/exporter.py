from typing import Callable

import numpy as np
from scipy import interpolate

from surface_analysis.points_to_mesh_converter import points_to_tris
from surface_analysis.points_to_mesh_converter import points_and_tris_to_mesh


GRID_SIZE = 0.015


def export_points_delaunay_stl(x, y, z, file_name):
    tris = points_to_tris(x, y)
    mesh = points_and_tris_to_mesh(x, y, z, tris)
    mesh.save(file_name)


def export_function_stl(
    x: np.ndarray,
    y: np.ndarray,
    func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    width,
    height,
    file_name: str,
):
    xmin = -width / 2
    xmax = width / 2
    ymin = -height / 2
    ymax = height / 2

    xcount = int(round((xmax - xmin) / GRID_SIZE))
    ycount = int(round((ymax - ymin) / GRID_SIZE))
    xi = np.linspace(xmin, xmax, xcount)
    yi = np.linspace(ymin, ymax, ycount)

    vertexes = np.ndarray((xi.size, yi.size, 3))
    for y in range(yi.size):
        for x in range(xi.size):
            vertexes[x, y, 0] = xi[x]
            vertexes[x, y, 1] = yi[y]
            x_value = xi[x]
            y_value = yi[y]
            x_array = np.array([x_value]).reshape((-1, 1))
            y_array = np.array([y_value]).reshape((-1, 1))
            vertexes[x, y, 2] = func(x_array, y_array)[0, 0]

    write_stl(file_name, vertexes)

def export_points_resampled_stl(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    width,
    height,
    file_name: str,
):
    tck = interpolate.bisplrep(x, y, z)

    xmin = -width / 2
    xmax = width / 2
    ymin = -height / 2
    ymax = height / 2

    xcount = int(round((xmax - xmin) / GRID_SIZE))
    ycount = int(round((ymax - ymin) / GRID_SIZE))
    xi = np.linspace(xmin, xmax, xcount)
    yi = np.linspace(ymin, ymax, ycount)
    zi = interpolate.bisplev(xi, yi, tck)

    vertexes = np.ndarray((xi.size, yi.size, 3))
    for y in range(yi.size):
        for x in range(xi.size):
            vertexes[x, y, 0] = xi[x]
            vertexes[x, y, 1] = yi[y]
            vertexes[x, y, 2] = zi[x, y]

    write_stl(file_name, vertexes)


def write_stl(file_name: str, vertexes: np.ndarray) -> None:
    with open(file_name, "w") as file:
        file.write("solid mirror\n")
        for y in range(vertexes.shape[1] - 1):
            for x in range(vertexes.shape[0] - 1):
                v0 = vertexes[x, y, :]
                v1 = vertexes[x + 1, y, :]
                v2 = vertexes[x + 1, y + 1, :]
                v3 = vertexes[x, y + 1, :]

                writeTri(file, v0, v1, v3)
                writeTri(file, v1, v2, v3)
        file.write("endsolid mirror\n")


def writeTri(file, v0, v1, v2):
    s0 = v1 - v0
    s1 = v2 - v0
    n = np.cross(s0, s1)
    n2 = n * n
    length = np.sqrt(sum(n2))
    n /= length
    file.write("facet normal %e %e %e\n  outer loop\n" % (n[0], n[1], n[2]))
    file.write("    vertex %e %e %e\n" % (v0[0], v0[1], v0[2]))
    file.write("    vertex %e %e %e\n" % (v1[0], v1[1], v1[2]))
    file.write("    vertex %e %e %e\n" % (v2[0], v2[1], v2[2]))
    file.write("  endloop\nendfacet\n")
