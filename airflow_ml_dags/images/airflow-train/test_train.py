import os

import numpy as np
from train import train

TEST_DIR = os.path.join("..", "test_data")


def test_train(tmpdir):
    pipeline = train(TEST_DIR)
