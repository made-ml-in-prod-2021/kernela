import pathlib
import pandas as pd
import click
import pickle


@click.command()
@ click.option("--data_dir")
@ click.option("--model_path")
@ click.option("--predict_path")
def predict(data_dir: str, model_path: str, predict_path: str):
    valid_datapath = pathlib.Path(data_dir) / "data.csv"

    features = pd.read_csv(valid_datapath, encoding="utf-8")

    with open(model_path, "rb") as model_dump:
        pipelien = pickle.load(model_dump)

    predicted = pipelien.predict(features.to_numpy())

    path_to_metrics = pathlib.Path(predict_path)
    path_to_metrics.parent.mkdir(exist_ok=True, parents=True)

    predicted_data = pd.DataFrame({"predicted_target": predicted})

    predicted_data.to_csv(predict_path, index=False, encoding="utf-8")


if __name__ == '__main__':
    predict()
