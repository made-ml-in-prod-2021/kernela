import os

import click
import pandas as pd
from pandas_profiling import ProfileReport


@click.command()
@click.option("--input_path", required=True)
@click.option("--report_dir", required=True)
def report(input_path: str, report_dir: str):
    features = pd.read_csv(input_path, encoding="utf-8")

    report = ProfileReport(features, minimal=True)
    repo_path = os.path.join(report_dir, "eda.html")
    os.makedirs(report_dir, exist_ok=True)

    report.to_file(repo_path)


if __name__ == '__main__':
    report()
