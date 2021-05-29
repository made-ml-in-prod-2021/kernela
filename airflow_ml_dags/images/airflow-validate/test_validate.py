import os

import pytest
from unittest.mock import patch
import numpy as np
from click.testing import CliRunner
from validate import validate

TEST_DIR = os.path.join("..", "test_data")


class DummpyPredictor:
    def predict(self, features):
        return np.ones(features.shape[0])


@pytest.fixture
def dummpy_load():
    def mocked_pickle_load(file_obj):
        return DummpyPredictor()
    return mocked_pickle_load


@ patch("validate.pickle.load")
def test_hello_world(mock_pickle_load, tmpdir, dummpy_load):
    mock_pickle_load.side_effect = dummpy_load

    dir = tmpdir.mkdir("data")
    model_path = dir.join("model.pickle")
    metric_file = dir.join("conf_matrix.txt")

    with open(model_path, "wb") as dummpy_dump:
        dummpy_dump.write(b"1")

    runner = CliRunner()
    result = runner.invoke(
        validate, ["--valid_dir", TEST_DIR, "--model_path", str(model_path), "--metric_file", str(metric_file)])

    assert result.exit_code == 0
    assert os.path.isfile(metric_file)

    conf_matrix = np.loadtxt(metric_file, encoding="utf-8")

    assert conf_matrix.shape == (2, 2)
