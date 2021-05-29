import pathlib
import pandas as pd
import click
import pickle

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


@click.command()
@ click.option("--train_dir")
@ click.option("--model_path")
@ click.option("--pickle_protocol", default=4, type=int)
def train(train_dir: str, model_path: str, pickle_protocol: int):
    train_datapath = pathlib.Path(train_dir) / "data.csv"
    target_datapath = train_datapath.parent / "target.csv"

    features = pd.read_csv(train_datapath, encoding="utf-8")
    target = pd.read_csv(target_datapath, encoding="utf-8")

    pipeline = Pipeline([("scaler", StandardScaler()),
                         ("predict", LogisticRegression())])

    pipeline.fit(features.to_numpy(), target.to_numpy().ravel())

    path_to_model = pathlib.Path(model_path)

    path_to_model.parent.mkdir(exist_ok=True, parents=True)

    with open(path_to_model, "wb") as dump_file:
        pickle.dump(pipeline, dump_file, protocol=pickle_protocol)


if __name__ == '__main__':
    train()
