import pathlib
import logging

import configargparse
from pandas_profiling import ProfileReport
import pandas as pd

import heat_diss


def main(args):
    logger = logging.getLogger()
    out_path = pathlib.Path(args.output_report)
    out_path.parent.mkdir(exist_ok=True, parents=True)
    data = pd.read_csv(args.input_data)
    data = data.infer_objects()
    profile = ProfileReport(data, title='Pandas Profiling Report', explorative=True)

    logger.info("save report to %s", out_path)
    profile.to_file(str(out_path))


if __name__ == "__main__":
    parser = configargparse.ArgumentParser()
    parser.add_argument("--config", is_config_file=True)
    parser.add_argument("--input_data", type=str, required=True)
    parser.add_argument("--output_report", type=str, required=True)

    args = parser.parse_args()

    main(args)
