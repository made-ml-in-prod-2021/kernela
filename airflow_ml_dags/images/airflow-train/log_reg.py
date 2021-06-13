import pathlib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


def train(train_dir: str):
    train_datapath = pathlib.Path(train_dir) / "data.csv"
    target_datapath = train_datapath.parent / "target.csv"

    features = pd.read_csv(train_datapath, encoding="utf-8")
    target = pd.read_csv(target_datapath, encoding="utf-8")

    pipeline = Pipeline([("scaler", StandardScaler()),
                         ("predict", LogisticRegression())])

    pipeline.fit(features.to_numpy(), target.to_numpy().ravel())

    return pipeline
