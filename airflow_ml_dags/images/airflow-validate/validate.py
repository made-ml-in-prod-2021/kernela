import pathlib
import os

import pandas as pd
import click
from sklearn import metrics
import mlflow
from mlflow.tracking import MlflowClient


def find_last_model(client, model_name: str):
    return sorted(client.search_model_versions(f"name='{model_name}'"),
                  key=lambda x: x.last_updated_timestamp, reverse=True)[0]


def load_model(model_info):
    model_uri = f"models:/{model_info.name}/{model_info.version}"
    loaded_model = mlflow.sklearn.load_model(model_uri)

    return loaded_model


@click.command()
@ click.option("--valid_dir")
@ click.option("--model_name", type=str, required=True)
@ click.option("--exp_name", type=str, required=True)
def mlflow_validate(valid_dir: str, model_name: str, exp_name: str):
    valid_datapath = pathlib.Path(valid_dir) / "data.csv"
    target_datapath = valid_datapath.parent / "target.csv"

    features = pd.read_csv(valid_datapath, encoding="utf-8")
    target = pd.read_csv(target_datapath, encoding="utf-8")

    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URL"])

    client = MlflowClient()

    last_model_metainfo = find_last_model(client, model_name)

    model = load_model(last_model_metainfo)

    experiment = mlflow.get_experiment_by_name(exp_name)

    if experiment is None:
        experiment_id = mlflow.create_experiment(exp_name)
        experiment = mlflow.get_experiment(experiment_id)

    mlflow.set_experiment(experiment.name)

    with mlflow.start_run() as run:
        predicted = model.predict(features.to_numpy())
        conf_matrix = metrics.confusion_matrix(
            target, predicted, normalize="true")

        mlflow.log_metric("true_negative", conf_matrix[0, 0])
        mlflow.log_metric("false_negative", conf_matrix[1, 0])
        mlflow.log_metric("true_positive", conf_matrix[1, 1])
        mlflow.log_metric("false_postive", conf_matrix[0, 1])

    client.transition_model_version_stage(name=last_model_metainfo.name,
                                          version=last_model_metainfo.version,
                                          stage="Production")


if __name__ == '__main__':
    mlflow_validate()
