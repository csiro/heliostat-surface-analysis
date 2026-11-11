import os
import pytest
import random

from heliostat_surface_analysis.loader.txt_loader import TXTLoader
from heliostat_surface_analysis.analysis_manager import AnalysisManager
from heliostat_surface_analysis.preprocessor.basic_preprocessor import BasicPreprocessor
from heliostat_surface_analysis.mesher.delaunay_mesher import DelaunayMesher
from heliostat_surface_analysis.analyser.fit_surface_analyser import FitSurfaceAnalyser
from heliostat_surface_analysis.aggregator.aggregator import WeightedMLEAggregator

def create_synthetic_paraboloid_scan_file(
    f: float,
    h: float,
    w: float,
    n: int,
    odir: str,
    seed: int | None = None,
) -> str:
    """
    Create a synthetic circular paraboloid point-cloud scan file.

    Parameters
    ----------
    f : float
        Focal length (m).
    h : float
        Height of facet (m).
    w : float
        Width of facet (m).
    n : int
        Number of points to sample from the surface.
    odir : str
        Output directory.
    seed : int | None
        Random seed for reproducible results.

    Returns
    -------
    str
        Output filename.
    """
    rng = random.Random(seed)

    os.makedirs(odir, exist_ok=True)

    fname = os.path.join(
        odir,
        "f%0.1f_h%0.1fm_w%0.1fm_n%d.txt" % (f, h, w, n),
    )

    with open(fname, "w") as ofile:
        for _ in range(n):
            x = rng.uniform(-0.5 * w, 0.5 * w)
            y = rng.uniform(-0.5 * h, 0.5 * h)
            z = (x**2 + y**2) / (4.0 * f)

            ofile.write(f"{x:e}\t{y:e}\t{z:e}\n")

    return fname

import os


def test_create_scan_file(tmp_path):
    """
    Verify that a synthetic paraboloid scan file is created and
    contains the expected number of points.
    """
    scan_file = create_synthetic_paraboloid_scan_file(
        f=50.0,
        h=3.0,
        w=3.0,
        n=1000,
        odir=tmp_path
    )

    assert os.path.exists(scan_file)

    with open(scan_file) as f:
        lines = f.readlines()

    assert len(lines) == 1000

def test_analyse_scan_file(tmp_path):
    """
    Verify that the synthetic paraboloid scan file can be analysed
    and that the analysis results are as expected.
    """
    focal_length = random.uniform(20.0, 100.0)
    n_points = [1000,10_000]
    scan_file_paths = []
    for n in n_points:
        scan_file_path = create_synthetic_paraboloid_scan_file(f=focal_length,h=3.0,w=3.0,n=n,odir=tmp_path)
        scan_file_paths.append(scan_file_path)

    loader = TXTLoader()
    preprocessor = BasicPreprocessor()
    mesher = DelaunayMesher({'max_aspect_ratio':10,'verbose':True})
    analyser = FitSurfaceAnalyser({"surface":"circular_paraboloid"})
    aggregator = WeightedMLEAggregator()
    for scan_file_path in scan_file_paths:
        print(f"Analysing scan file: {scan_file_path}")
        result = AnalysisManager.analyse_scan(scan_file_path,loader,preprocessor,mesher,analyser,aggregator,output_dir=None,plot=False,write_stls=False)
        f = 1/4./result["coeff: a(x^2 + y^2)"]
        sigma_mrad = result["aggregate"]*1e3
        print("f = %0.1fm, sigma = %0.2fmrad"%(f,sigma_mrad))

        assert f == pytest.approx(focal_length, rel=1e-2)
        assert sigma_mrad < 1.0  