import pathlib

import click
import pandas as pd
from sklearn.model_selection import train_test_split


@click.command()
@click.option("--input_dir", required=True)
@click.option("--out_dir", required=True)
@click.option("--seed", default=200, type=int)
@click.option("--train_size", default=0.8, type=float)
def split(input_dir: str, out_dir: str, seed: int, train_size: float):
    features_path = pathlib.Path(input_dir) / "data.csv"
    target_path = pathlib.Path(input_dir) / "target.csv"

    features = pd.read_csv(features_path, encoding="utf-8")
    target = pd.read_csv(target_path, encoding="utf-8")

    train, test, train_traget, test_target = train_test_split(
        features, target, random_state=seed, train_size=train_size)

    out_dir_path = pathlib.Path(out_dir)

    train_dir = out_dir_path / "train"

    train_dir.mkdir(exist_ok=True, parents=True)

    train.to_csv(train_dir / "data.csv", index=False)
    train_traget.to_csv(train_dir / "target.csv", index=False)

    test_dir = out_dir_path / "test"

    test_dir.mkdir(exist_ok=True, parents=True)

    test.to_csv(test_dir / "data.csv", index=False)
    test_target.to_csv(test_dir / "target.csv", index=False)


if __name__ == '__main__':
    split()
