import os

import numpy as np
import click
from sklearn import datasets


@click.command()
@click.option("--out_dir", required=True)
def download(out_dir: str):
    features, target = datasets.make_classification(200, n_informative=10)

    os.makedirs(out_dir, exist_ok=True)

    delimiter = ","

    np.savetxt(os.path.join(out_dir, "data.csv"), features, delimiter=delimiter,
               header=f'{delimiter}'.join(
                   [f"feature_{i}" for i in range(1, features.shape[1] + 1)]),
               encoding="utf-8", comments="")

    np.savetxt(os.path.join(out_dir, "target.csv"), target, delimiter=delimiter,
               header="target", encoding="utf-8", comments="")


if __name__ == '__main__':
    download()
