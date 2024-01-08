import argparse
import toml

# add the 'src' directory to the path so that surface_analysis can be imported (only required when running git repo code directly and outside of poetry)
import os,sys
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(src_dir)
sys.path.insert(0,src_dir)

from heliostat_surface_analysis.config.config import Config
from heliostat_surface_analysis.analysis_manager import AnalysisManager

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
        prog="heliostat_surface_analysis",
        description="Analyse point cloud measurements of surfaces"
    )
    parser.add_argument("config", type=str, help="Config file")
    parser.add_argument("input_dir", type=str, help="Path to scans directory for processing")
    parser.add_argument("output_dir", type=str, help="Path to output analysis results")
    parser.add_argument("--plot", action='store_true')
    parser.add_argument("--stl", action='store_true')
    return parser.parse_args()

def modify_file_paths(params,dir):
    # any additional file path variables should be listed here
    file_path_variables = ['focal_length_file']
    for k,v in params.items():
        if k in file_path_variables and isinstance(v,str):
            # this test below ensures we don't modify paths to files that can already be found
            if not os.path.exists(v):
                params[k] = os.path.join(dir,v)
        elif isinstance(v,dict):
            modify_file_paths(v,dir)

def load_config(file_path: str) -> Config:
    config_dict = toml.load(file_path)
    # file path variables are allowed to be provided relative to the config.toml parent directory, and we modify these paths in config_dict here
    dir = os.path.dirname(os.path.abspath(file_path))
    for groupName,groupDict in config_dict.items():
        modify_file_paths(groupDict,dir)
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
