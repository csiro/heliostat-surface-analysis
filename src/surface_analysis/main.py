import argparse

import toml

from surface_analysis.config.config import Config
from surface_analysis.analysis_manager import AnalysisManager

import typing

def main():
    args = parse_args()
    config = load_config(args.config)
    validate_config(config)

    analysis_manager = AnalysisManager()
    analysis_manager.analyze_scans(
        config,
        args.input_dir,
        args.output_dir,
        args.plot
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="poetry run python src/main.py",
        description="Analyse point cloud measurements of surfaces"
    )
    parser.add_argument("config", type=str, help="Config file")
    parser.add_argument("input_dir", type=str, help="Path to scans directory for processing")
    parser.add_argument("output_dir", type=str, help="Path to output analysis results")
    parser.add_argument("--plot", action='store_true')
    return parser.parse_args()


def load_config(file_path: str) -> Config:
    config_dict = toml.load(file_path)
    return Config(**config_dict)

def validate_config(config: Config) -> None:
    return

if __name__ == "__main__":
    main()
