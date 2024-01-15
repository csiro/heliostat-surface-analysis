# heliostat-surface-analysis

A Python package for post-processing (e.g. slope error determination) point cloud measurements of mirror surfaces such as heliostat facets.

## Description

The post-processing of mirror surfaces is broken into a sequence of stages:

1. loading
2. preprocessing
3. meshing
4. analysis
5. aggregation

The user provides a set of ASCII text files containing the x, y and z coordinates of the point cloud data obtained from surface metrology measurements (one file per mirror surface).
The format of the files (e.g. delimiters, units) can be taken into consideration by the loader.
A preprocessor can be applied to ensure the positioning of the points in the coordinate system is correct (i.e. basin of mirror at origin with normal in the the positive z direction).
A 3D surface mesh is then generated from the points.
Currently two meshers are available:

1. Regular grid using B-spline interpolation
2. Unstructured grid using Delaunay triangulation

The B-spline method often needs to apply significant smoothing, such that the resultant meshed surface doesn't pass exactly through the original data points.
For this reason the Delaunay method is preferred as the mesh vertices are constructured using the original data points.
When using the Delaunay mesher it is important to filter out mesh facets with high aspect ratio, as the normal direction of these facets is highly sensitive to small errors in the data point coordinates.

Once the mesh has been generated, the slope error distribution over the mirror surface can then determined using one of two analysers:

1. Fit surface (planar, paraboloidal or deformed paraboloidal)
2. Known focal length


## Getting Started

### Dependencies

heliostat-surface-analysis requires Python version 3.8.10 or greater and has been successfuly used on Windows 10, Windows 11, macOS and Ubuntu 20.04.
A number of third-party Python modules are utilised:

| Module     | Minimum version  |
| :--------: | :--------------: |
| numpy      | 1.23.3           |
| scipy      | 1.10.1           |
| pandas     | 1.4.4            |
| matplotlib | 3.1.2            |
| nlopt      | 2.7.1            |
| pydantic   | 2.1.1            |
| numpy-stl  | 2.13.1           |
| toml       | 0.10.2           |

These module dependencies are automatically installed when installing heliostat-surface-analysis via pip (see below).

### Installing

The source code for heliostat-surface-analysis is stored in the following BitBucket repository:

https://bitbucket.csiro.au/projects/HELIO/repos/heliostat-surface-analysis

If you have read access to the repository, it can be cloned via:

```
git clone ssh://git@bitbucket.csiro.au:7999/helio/heliostat-surface-analysis.git
```

or

```
git clone https://bitbucket.csiro.au/scm/helio/heliostat-surface-analysis.git
```

The module can be loaded directly from the repository directory by including the top level directory path in the PYTHONPATH environment variable.
Alternatively, heliostat-surface-analysis can be installed via PyPI:

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
When installing with PyPI, the `Scripts` directory of your Python distribution can be added to `PATH` for convenient access to the command-line tools supplied with heliostat-surface-analysis.  The location of the Python `Scripts` directory (e.g. `c:\users\username\appdata\roaming\python\python39\scripts\`) that was used for the package installation can be found via:

```
pip show -f heliostat-surface-analysis | more
```

### Usage

heliostat-surface-analysis can be used either from the command-line or by loading the module into your own Python scripts or notebooks.
The command-line tool `heliostat_surface_analysis` is installed to the Python scripts directory when installing with PyPI.
The usage of this tool can be seen via:

```
> heliostat_surface_analysis --help
usage: heliostat_surface_analysis [-h] [--plot] [--stl] config input_dir output_dir

Analyse point cloud measurements of surfaces

positional arguments:
  config      Config file
  input_dir   Path to scans directory for processing
  output_dir  Path to output analysis results

optional arguments:
  -h, --help  show this help message and exit
  --plot
  --stl
```

When using heliostat-surface-analysis from Python scripts or notebooks, the parent module can be loaded via:

```
import heliostat_surface_analysis
```

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
See the LICENSE file for full terms of the license.
