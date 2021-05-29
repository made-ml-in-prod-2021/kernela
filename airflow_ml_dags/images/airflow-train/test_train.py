import os
import pickle

import numpy as np
from click.testing import CliRunner
from train import train

TEST_DIR = os.path.join("..", "test_data")


def test_hello_world(tmpdir):
    modle_path = tmpdir.mkdir("data").join("model.pickle")
    runner = CliRunner()
    result = runner.invoke(
        train, ["--train_dir", TEST_DIR, "--model_path", str(modle_path)])

    assert result.exit_code == 0

    with open(modle_path, "rb") as dump_file:
        pickle.load(dump_file)
