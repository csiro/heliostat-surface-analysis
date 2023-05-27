import argparse
import os

import toml

from surface_analysis.config.config import Config
from surface_analysis.analysis_manager import AnalysisManager


# MANIFEST_FILE = "designfocallengths.txt"


# Loader: Default
# Preprocessor: Basic - add known size mode for z rotation
# Analyser: Supplied reference surface, mesh comparison (mesh has filtering step)
# Comparison: slope error
# Summariser: RMS


def main():
    args = parse_args()
    config = load_config(args.config)

    # validate_config(config)
    # Want a step at the start to validate that the workflow is valid
    # i.e. the right parts can plug together

    # Don't want to assume design focal lengths yet
    # design_focal_lengths = load_design_focal_lengths(args.input_dir)
    # scan_files = list_scans(args.input_dir)

    # validate_scans(design_focal_lengths, scan_files)

    analysis_manager = AnalysisManager()
    analysis_manager.analyse_scans(
        config,
        args.input_dir,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="poetry run python src/main.py",
        description="Analyse point cloud measurements of surfaces"
    )
    parser.add_argument("config", type=str, help="Config file")
    parser.add_argument("input_dir", type=str, help="Path to scans directory for processing")
    parser.add_argument("output_dir", type=str, help="Path to output analysis results")
    return parser.parse_args()


def load_config(file_path: str) -> Config:
    config_dict = toml.load(file_path)
    print(config_dict)
    return Config(**config_dict)


# def validate_config(config: Config) -> None:
#     if config.loader
# def load_design_focal_lengths(scans_dir: str) -> dict[str, float]:
#     manifest_path = os.path.join(scans_dir, MANIFEST_FILE)

#     focal_lengths = {}
#     with open(manifest_path, "r") as manifest_file:
#         for line in manifest_file.readlines():
#             parts = line.split()
#             scan_name = parts[0]
#             design_focal_length = float(parts[1])
#             focal_lengths[scan_name] = design_focal_length

#     return focal_lengths


# def list_scans(scans_dir: str) -> list[str]:
#     entries = os.listdir(scans_dir)

#     files = []
#     for entry in entries:
#         path = os.path.join(scans_dir, entry)
#         if os.path.isfile(path):
#             files.append(entry)

#     if MANIFEST_FILE not in files:
#         print(f"ERROR: No {MANIFEST_FILE} found in {scans_dir}")
#         exit()
#     else:
#         files.remove(MANIFEST_FILE)

#     return files


# def validate_scans(
#     design_focal_lengths: dict[str, float],
#     scan_files: list[str],
# ) -> None:
#     for scan_file in scan_files:
#         scan_name = scan_file.split(".")[0]
#         if scan_name not in design_focal_lengths:
#             print(f"ERROR: Scan {scan_name} not in {MANIFEST_FILE}")
#             exit()


if __name__ == "__main__":
    main()
