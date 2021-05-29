import os

import numpy as np
from click.testing import CliRunner
from download import download


def test_hello_world(tmpdir):
    out_dir = tmpdir.mkdir("data")
    runner = CliRunner()
    result = runner.invoke(download, ["--out_dir", str(out_dir)])
    assert result.exit_code == 0
    feature_path = out_dir / "data.csv"
    target_path = out_dir / "target.csv"
    assert os.path.isfile(feature_path)
    assert os.path.isfile(target_path)

    features = np.loadtxt(feature_path,
                          delimiter=",", skiprows=1, encoding="utf-8")

    target = np.loadtxt(target_path,
                        delimiter=",", skiprows=1, encoding="utf-8")

    assert features.shape[0] == target.shape[0]
