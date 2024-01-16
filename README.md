# heliostat-surface-analysis

A Python package for post-processing (e.g. slope error determination) point cloud measurements of mirror surfaces such as heliostat facets.

## Description

The post-processing of mirror surfaces is broken into a sequence of stages:

1. loading
2. preprocessing
3. meshing
4. analysis
5. aggregation

The user provides a set of ASCII text files containing the *x*, *y* and *z* coordinates of the point cloud data obtained from surface metrology measurements (one file per mirror surface).
The format of the files (e.g. delimiters, units) can be taken into consideration by the loader.
A preprocessor can be applied to ensure the positioning of the points in the coordinate system is correct (i.e. basin of mirror at origin with normal in the the positive *z* direction).
A 3D surface mesh is then generated from the points.
Currently two meshers are available:

1. Regular grid using B-spline interpolation
2. Unstructured grid using Delaunay triangulation

The B-spline method often needs to apply significant smoothing, resulting in a meshed surface that doesn't pass exactly through the original data points.
For this reason the Delaunay method is preferred as the mesh vertices are constructured using the original data points.
When using the Delaunay mesher, however, it is important to filter out mesh facets with high aspect ratio as the normal direction of these facets is highly sensitive to small errors in the data point coordinates.

Once the mesh has been generated, the slope error distribution over the mirror surface can then determined by comparing the normal vectors from the mesh facets generated from the point cloud data with a reference surface.
The reference surface can be created using one of these two methods:

1. Known focal length paraboloid
2. Fit surface (planar, paraboloidal or deformed paraboloidal)

The first method uses a paraboloidal mirror of a particular fixed focal length (e.g. the design focal length) as the reference surface.
This is useful for determining the slope error distribution relative to the intended design for the facet.
The fit surface option apply a linear least squares method to fit a surface (planar, paraboloid or deformed paraboloid) to the point cloud data.
For a paraboloidal surface, this allows the focal length that best describes the point cloud data to be found and used for calculating the slope error distribution.
Typically the resultant slope error using this approach is lower compared to the known focal length method, as the focal length error has been eliminated.
The deformed paraboloidal surface is described using the equations presented by [Cumpston and Coventry (2017)](http://dx.doi.org/10.1063/1.4984356), and allows curvature and twist to be included in the reference paraboloidal surface.

The final step is aggregating the slope error distribution over the facet surface to obtain a single slope error representative of the whole surface.
Various aggregation methods have been implemented, including:

1. Mean
2. RMS
3. Area-weighted RMS

The area-weighted RMS method weights the slope error distribution according to the mesh facet area.
This is the recommended method when using Delaunay meshing where the triangular mesh facet sizes can have a large variation if the point cloud data is not uniformly sampled from over the mirror surface.

## Getting Started

### Dependencies

*heliostat-surface-analysis* requires Python version 3.8.10 or greater and has been successfuly used on Windows 10, Windows 11, macOS and Ubuntu 20.04.
A number of third-party Python modules are utilised:

| Module      | Minimum version  |
| :---------: | :--------------: |
| numpy       | 1.23.3           |
| scipy       | 1.10.1           |
| pandas      | 1.4.4            |
| matplotlib  | 3.1.2            |
| nlopt       | 2.7.1            |
| pydantic    | 2.1.1            |
| numpy-stl   | 2.13.1           |
| toml        | 0.10.2           |
| progressbar | 2.5              |

These module dependencies are automatically installed when installing *heliostat-surface-analysis* via pip (see below).

### Installing

The source code for *heliostat-surface-analysis* is stored in the following BitBucket repository:

https://bitbucket.csiro.au/projects/HELIO/repos/heliostat-surface-analysis

If you have read access to the repository, it can be cloned via:

```
git clone ssh://git@bitbucket.csiro.au:7999/helio/heliostat-surface-analysis.git
```

or

```
git clone https://bitbucket.csiro.au/scm/helio/heliostat-surface-analysis.git
```

The module can be loaded directly from the repository directory by including the top level directory path in the `PYTHONPATH` environment variable.
Alternatively, *heliostat-surface-analysis* can be installed via PyPI:

```
cd heliostat-surface-analysis
pip install .
```
or used within a poetry virtual environment:

```
cd heliostat-surface-analysis
poetry install
poetry shell
```
When installing with PyPI, the scripts directory of your Python distribution can be added to `PATH` for convenient access to the command-line tools supplied with *heliostat-surface-analysis*.  The location of the Python scripts directory (e.g. `c:\users\username\appdata\roaming\python\python39\scripts\`) that was used for the package installation can be found via:

```
pip show -f heliostat-surface-analysis | more
```

### Usage

*heliostat-surface-analysis* can be used either from the command-line or by loading the module into your own Python scripts or notebooks.

#### Command-line interface

The command-line tool `heliostat_surface_analysis` is installed to the Python scripts directory when installing with PyPI.
The usage of this tool can be seen with the `--help` option:

```
> heliostat_surface_analysis --help
usage: heliostat_surface_analysis [-h] [--plot] [--stl] config input_dir output_dir

Analyse point cloud measurements of surfaces

positional arguments:
  config      config file
  input_dir   path to scans directory for processing
  output_dir  path to a directory for writing output files

optional arguments:
  -h, --help  show this help message and exit
  --plot      display plots of point cloud data and mesh with slope error analysis
  --stl       write meshes to STL files in the output directory
```

A number of sample cases for the command-line interface are provided in the examples directory of the BitBucket repository:

https://bitbucket.csiro.au/projects/HELIO/repos/heliostat-surface-analysis/browse/examples/command_line

To run the 'circular_paraboloid_peg' case without displaying plots and writing the meshes to STL files, for example, the following command can be used:

```
> cd examples\command_line\circular_paraboloid_peg
> heliostat_surface_analysis config.toml scans output --stl
```

Note that the `heliostat_surface_analysis` tool doesn't have to be run from the directory containing the `config.toml` file.
For example the 'circular_paraboloid_peg' case can be run from its parent directory via:

```
> cd examples\command_line
> heliostat_surface_analysis config.toml circular_paraboloid_peg\scans circular_paraboloid_peg\output --stl
```

This is useful for running parametric studies organised by directory.

#### Python scripting

When using *heliostat-surface-analysis* from Python scripts or notebooks, the parent module can be loaded via:

```
import heliostat_surface_analysis
```
A demonstration of using *heliostat-surface-analysis* via a Python notebook has been provided in the examples directory of the BitBucket repository:

https://bitbucket.csiro.au/projects/HELIO/repos/heliostat-surface-analysis/browse/examples/notebooks/example_analysis.ipynb

## Help

Documentation is not currently available.
Please see the examples.

## Authors

Mike Collins - mike.collins@csiro.au  
Daniel Potter - daniel.potter@csiro.au  
Calum Acutt (previously at CSIRO)  

## Version History

* 0.1
    * Initial Release

## License

CSIRO Open Source Software Licence v1.0 (Based on MIT/BSD Open Source Licence).
See the LICENSE file for full terms of the license:

https://bitbucket.csiro.au/projects/HELIO/repos/heliostat-surface-analysis/browse/LICENSE
