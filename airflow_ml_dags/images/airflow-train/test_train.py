import os

import numpy as np
from sklearn.pipeline import Pipeline
import pandas as pd
from log_reg import train

TEST_DIR = os.path.join("..", "test_data")


def test_train(tmpdir):
    pipeline = train(TEST_DIR)

    features = pd.read_csv(os.path.join(TEST_DIR, "data.csv"))
    target = pd.read_csv(os.path.join(TEST_DIR, "target.csv"))

    assert len(pipeline.predict(features)) == target.shape[0]
