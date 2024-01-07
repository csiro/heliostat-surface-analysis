# heliostat-surface-analysis

A Python package for analysing point cloud measurements of mirror surfaces such as heliostat facets.

## Description


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
Alternatively, heliostat-surface-analysis can be installed via pip:

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

### Usage

The parent module can be loaded via:

```
module load surface_analysis
```

## Help

Documentation is not currently available.
Please see the examples.

## Authors

Mike Collins - mike.collins@csiro.au  
Daniel Potter - daniel.potter@csiro.au  
Calum Acutt (ex CSIRO)  

## Version History

* 0.1
    * Initial Release

## License

heliostat-surface-analysis is currently intended for internal CSIRO use only.
