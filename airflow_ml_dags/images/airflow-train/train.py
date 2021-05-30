import pathlib
import pandas as pd
import click
import os

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

import mlflow


@click.command()
@ click.option("--train_dir")
@ click.option("--exp_name", type=str, required=True)
def mlflow_train(train_dir: str, exp_name: str):
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URL"])

    experiment = mlflow.get_experiment_by_name(exp_name)

    if experiment is None:
        experiment_id = mlflow.create_experiment(exp_name)
        experiment = mlflow.get_experiment(experiment_id)

    mlflow.set_experiment(experiment.name)

    mlflow.sklearn.autolog()

    with mlflow.start_run() as run:
        pipeline = train(train_dir)


def train(train_dir: str):
    train_datapath = pathlib.Path(train_dir) / "data.csv"
    target_datapath = train_datapath.parent / "target.csv"

    features = pd.read_csv(train_datapath, encoding="utf-8")
    target = pd.read_csv(target_datapath, encoding="utf-8")

    pipeline = Pipeline([("scaler", StandardScaler()),
                         ("predict", LogisticRegression())])

    pipeline.fit(features.to_numpy(), target.to_numpy().ravel())

    return pipeline


if __name__ == '__main__':
    mlflow_train()
