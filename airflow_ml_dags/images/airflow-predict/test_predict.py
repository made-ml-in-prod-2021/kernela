import os

import pytest
from unittest.mock import patch
import numpy as np
import pandas as pd
from click.testing import CliRunner
from predict import predict

TEST_DIR = os.path.join("..", "test_data")


class DummpyPredictor:
    def predict(self, features):
        return np.ones(features.shape[0])


@pytest.fixture
def dummpy_load():
    def mocked_pickle_load(file_obj):
        return DummpyPredictor()
    return mocked_pickle_load


@ patch("predict.pickle.load")
def test_hello_world(mock_pickle_load, tmpdir, dummpy_load):
    mock_pickle_load.side_effect = dummpy_load

    dir = tmpdir.mkdir("data")
    model_path = dir.join("model.pickle")
    pred_file = dir.join("predicted.csv")

    with open(model_path, "wb") as dummpy_dump:
        dummpy_dump.write(b"1")

    runner = CliRunner()
    result = runner.invoke(
        predict, ["--data_dir", TEST_DIR, "--model_path", str(model_path), "--predict_path", str(pred_file)])

    assert result.exit_code == 0
    assert os.path.isfile(pred_file)

    predicted = pd.read_csv(pred_file)
    target = pd.read_csv(os.path.join(TEST_DIR, "target.csv"))

    assert predicted.shape[0] == target.shape[0]
