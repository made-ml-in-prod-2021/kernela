import pathlib
import logging

from pandas_profiling import ProfileReport
import pandas as pd
import hydra

import heat_diss
from config import ReportConfig


@hydra.main(config_name="report_config")
def main(config: ReportConfig):
    orig_wd = pathlib.Path(hydra.utils.get_original_cwd())
    logger = logging.getLogger()
    out_path = orig_wd / config.output_report
    out_path.parent.mkdir(exist_ok=True, parents=True)
    data = pd.read_csv(orig_wd / config.input_zip)
    data = data.infer_objects()
    profile = ProfileReport(data, title='Pandas Profiling Report', explorative=True)

    logger.info("Save report to %s", out_path)
    profile.to_file(str(out_path))


if __name__ == "__main__":
    main()
