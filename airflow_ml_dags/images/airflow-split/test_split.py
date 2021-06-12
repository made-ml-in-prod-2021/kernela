import os

import numpy as np
from click.testing import CliRunner
from split import split

TEST_DIR = os.path.join("..", "test_data")


def test_split(tmpdir):
    out_dir = tmpdir.mkdir("data")
    runner = CliRunner()
    result = runner.invoke(
        split, ["--input_dir", TEST_DIR, "--out_dir", str(out_dir)])

    assert result.exit_code == 0

    for split_dir in ("train", "test"):
        feature_path = out_dir / split_dir / "data.csv"
        target_path = out_dir / split_dir / "target.csv"

        assert os.path.isfile(feature_path)
        assert os.path.isfile(target_path)
