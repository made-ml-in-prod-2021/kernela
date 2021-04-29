import os

import yaml
import pytest

import numpy as np
import pandas as pd
import heat_diss
from heat_diss.preprocessing import get_numeric_transform

SEED = 10

np.random.seed(SEED)

CONFIG_PATH = os.path.join("configs", "train", "numeric_scaler.yml")


@pytest.fixture
def numeric_config():
    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)


@pytest.fixture
def numeric_data():
    return pd.DataFrame(np.random.random((10, 10)))


def test_scaler(numeric_config, numeric_data):
    numeric_transformer = get_numeric_transform(numeric_data.columns, **numeric_config)

    transformed = numeric_transformer.fit_transform(numeric_data)

    assert np.allclose(transformed.mean(axis=0), 0)
    assert np.allclose(transformed.std(axis=0), 1)
