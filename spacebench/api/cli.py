""" Command-line client """

import argparse
from spacebench.api.dataverse import DataverseAPI
import spacebench.datasets.error_sampler as err
from spacebench.datasets.datasets import DatasetGenerator

parser = argparse.ArgumentParser()

parser.add_argument("predictor", choices=['xgboost', 'nn'], 
                    help="The model predictor algorithms")
parser.add_argument("datatype", choices=['binary', 'continuous'], 
                    help='Type of data: binary or continuous')
parser.add_argument("seed", type=int, help='Random seed')
parser.add_argument('--output_path', type=str, help='Path to save the data file')


def main():
    args = parser.parse_args()

    # set random seed
    err.set_random_seed(args.seed)

    # download data

    dvapi = DataverseAPI()
    dvapi.download_data(args.predictor, args.datatype, args.output_path)

    print(dvapi.core_data_loc)

    generator = DatasetGenerator.from_json(
         dvapi.core_data_loc)
    dataset = generator.make_dataset()

    dataset.save_dataset(args.output_path)
    print("Dataset sampling completed.")


if __name__ == "__main__":
    main()