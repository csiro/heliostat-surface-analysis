import argparse
import tomllib
import pandas as pd

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

    analysis_results = AnalysisManager.analyse_scans(
        config,
        args.input_dir,
        args.output_dir,
        args.plot,
        args.stl
    )

    # make a pandas dataframe with the analysis_results
    if len(analysis_results)>0:
        labels = [ key for key in analysis_results[0] ]
        analysis_results_dict = {}
        for label in labels:
            analysis_results_dict[label] = []
        for result in analysis_results:
            for label in labels:
                analysis_results_dict[label].append(result[label])
        df = pd.DataFrame.from_dict(analysis_results_dict)
        print(df)
        output_file_path = os.path.join(args.output_dir,"analysis_results.xlsx")
        df.to_excel(output_file_path)
        print("analysis results have been writen to file: %s"%output_file_path)
    print("Done.")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="heliostat_surface_analysis",
        description="Analyse point cloud measurements of surfaces"
    )
    parser.add_argument("config", type=str, help="config file")
    parser.add_argument("input_dir", type=str, help="path to scans directory for processing")
    parser.add_argument("output_dir", type=str, help="path to a directory for writing output files")
    parser.add_argument("--plot", action='store_true', help="display plots of point cloud data and mesh with slope error analysis")
    parser.add_argument("--stl", action='store_true', help="write meshes to STL files in the output directory")
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
    with open(file_path, "rb") as f:
        config_dict = tomllib.load(f)
    # file path variables are allowed to be provided relative to the config.toml parent directory, and we modify these paths in config_dict here
    config_dir = os.path.dirname(os.path.abspath(file_path))
    for _,group_dict in config_dict.items():
        modify_file_paths(group_dict,config_dir)
    
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
