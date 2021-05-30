import pathlib
import pandas as pd
import click
import pickle
import numpy as np

from airflow import airflow
from sklearn import metrics


@click.command()
@ click.option("--valid_dir")
@ click.option("--model_path")
@ click.option("--metric_file")
def validate(valid_dir: str, model_path: str):
    valid_datapath = pathlib.Path(valid_dir) / "data.csv"
    target_datapath = valid_datapath.parent / "target.csv"

    features = pd.read_csv(valid_datapath, encoding="utf-8")
    target = pd.read_csv(target_datapath, encoding="utf-8")

    with open(model_path, "rb") as model_dump:
        pipelien = pickle.load(model_dump)

    predicted = pipelien.predict(features.to_numpy())
    conf_matrix = metrics.confusion_matrix(target, predicted, normalize="true")

    path_to_metrics = pathlib.Path(metric_file)
    path_to_metrics.parent.mkdir(exist_ok=True, parents=True)
    np.savetxt(path_to_metrics, conf_matrix, encoding="utf-8")


if __name__ == '__main__':
    validate()
