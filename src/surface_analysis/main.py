import argparse
import toml

# add the 'src' directory to the path so that surface_analysis can be imported (only required when running git repo code directly and outside of poetry)
import os,sys
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(src_dir)
sys.path.insert(0,src_dir)

from surface_analysis.config.config import Config
from surface_analysis.analysis_manager import AnalysisManager

import typing

def main():
    args = parse_args()
    validate_args(args)
    config = load_config(args.config)
    validate_config(config)

    AnalysisManager.analyse_scans(
        config,
        args.input_dir,
        args.output_dir,
        args.plot,
        args.stl
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
    parser.add_argument("--stl", action='store_true')
    return parser.parse_args()


def load_config(file_path: str) -> Config:
    config_dict = toml.load(file_path)
    return Config(**config_dict)

def validate_config(config: Config) -> None:
    return
   
def validate_args(args: argparse.Namespace) -> None:
    if not os.path.isdir(args.input_dir):
        raise RuntimeError("input_dir: %s doesn't exist"%args.input_dir)
    if not os.path.isdir(args.output_dir):
        print("creating output_dir: %s as it doesn't exist"%args.output_dir)
        os.makedirs(args.output_dir)

if __name__ == "__main__":
    main()
