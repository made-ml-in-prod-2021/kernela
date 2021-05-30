import os
import pathlib

import pandas as pd
import click
import mlflow.pyfunc
import mlflow
import numpy as np


def load_data(data_dir: str, filename: str = "data.csv"):
    valid_datapath = pathlib.Path(data_dir) / filename
    features = pd.read_csv(valid_datapath, encoding="utf-8")

    return features


def save_prediction(predicted: np.ndarray, prediction_path: str):
    path_to_pred = pathlib.Path(prediction_path)
    path_to_pred.parent.mkdir(exist_ok=True, parents=True)
    predicted_data = pd.DataFrame({"predicted_target": predicted})
    predicted_data.to_csv(path_to_pred, index=False, encoding="utf-8")


@click.command()
@ click.option("--data_dir")
@ click.option("--model_name")
@ click.option("--predict_path")
@ click.option("--stage", default="Production")
def mlflow_predict(data_dir: str, model_name: str, predict_path: str, stage: str):
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URL"])

    model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{stage}")

    features = load_data(data_dir)

    predicted = model.predict(features.to_numpy())

    save_prediction(predicted, predict_path)


if __name__ == '__main__':
    mlflow_predict()
