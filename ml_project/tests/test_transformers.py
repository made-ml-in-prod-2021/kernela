from heat_diss.preprocessing.preprocess import get_binary_transfomer
import os
from scipy.sparse.construct import random

import yaml
import pytest
import random

import numpy as np
import pandas as pd
from faker import Faker
from heat_diss.preprocessing import get_numeric_transform, get_categorical_transfomer

SEED = 10
CATEGORICAL_DATA_SIZE = 20

Faker.seed(SEED)
random.seed(SEED)
np.random.seed(SEED)

NUMERIC_DATA_TRANSFORM_CONFIG = os.path.join("configs", "train", "standard_scaler.yml")
CAT_DATA_TRANSFORMER_CONFIG = os.path.join("configs", "train", "one_hot.yml")
BIN_DATA_TRANSFORMER_CONFIG = os.path.join("configs", "train", "binary_encoder.yml")


@pytest.fixture
def numeric_config():
    with open(NUMERIC_DATA_TRANSFORM_CONFIG, "r") as file:
        return yaml.safe_load(file)


@pytest.fixture
def bin_config():
    with open(BIN_DATA_TRANSFORMER_CONFIG, "r") as file:
        return yaml.safe_load(file)


@pytest.fixture
def cat_config():
    with open(CAT_DATA_TRANSFORMER_CONFIG, "r") as file:
        return yaml.safe_load(file)


@pytest.fixture
def numeric_data():
    return pd.DataFrame(np.random.normal((10, 2)))


@pytest.fixture
def categorical_data(faker):
    rows = []
    for _ in range(CATEGORICAL_DATA_SIZE):
        rows.append({"color": faker.color(), "bank": faker.bank_country()})

    return pd.DataFrame.from_records(rows)


@pytest.fixture
def binarized_data(faker):
    rows = 20
    col1 = [random.choice(["val1", "val2"]) for _ in range(rows)]
    col2 = [random.choice([4, 5]) for _ in range(rows)]

    return pd.DataFrame({"bin1": col1, "bin2": col2})


def test_scaler(numeric_config, numeric_data):
    numeric_transformer = get_numeric_transform(numeric_data.columns, **numeric_config)

    transformed = numeric_transformer.fit_transform(numeric_data)

    assert np.allclose(transformed.mean(axis=0), 0)
    assert np.allclose(transformed.std(axis=0), 1)


def test_categorical_transfomer(cat_config, categorical_data):
    cat_transformer = get_categorical_transfomer(categorical_data.columns, **cat_config)

    transformed = cat_transformer.fit_transform(categorical_data)

    total_unique_values = 0
    for col in categorical_data.columns:
        total_unique_values += len(categorical_data[col].unique())

    assert transformed.shape[0] == categorical_data.shape[0]
    assert transformed.shape[1] == total_unique_values
    assert (transformed.sum(axis=1) == categorical_data.shape[1]).all()


def test_custom_transformer(bin_config, binarized_data):
    bin_transformer = get_binary_transfomer(binarized_data.columns, **bin_config)

    transformed = bin_transformer.fit_transform(binarized_data)

    assert transformed.shape == binarized_data.shape
    assert (np.unique(transformed) == (0, 1)).all()
