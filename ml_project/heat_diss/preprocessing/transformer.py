from collections import defaultdict

from sklearn.base import TransformerMixin
import numpy as np
import pandas as pd


class BinaryEncoder(TransformerMixin):
    """Encode features with tow unique values
    """

    def __init__(self, ignore_unknown: bool = False, dtype: str = "float"):
        super().__init__()
        self._ignore_unknown = ignore_unknown
        self._dtype = dtype
        self._encoder = defaultdict(dict)

    def fit(self, X, y=None):
        if isinstance(X, pd.DataFrame) or isinstance(X, pd.Series):
            X = X.to_numpy()

        for i in range(X.shape[1]):
            uniq_values = np.unique(X[:, i])
            if len(uniq_values) != 2:
                raise ValueError(f"Feature at position {i} is not binary")

            self._encoder[i] = {uniq_value: i for i, uniq_value in enumerate(uniq_values)}

    def get_params(self, **kwarg):
        return {"ignore_unknown": self._ignore_unknown, "dtype": self._dtype}

    def fit_transform(self, X, y, **fit_params):
        self.fit(X, y)
        return self.transform(X)

    def transform(self, features):
        if features.shape[1] != len(self._encoder):
            raise ValueError(f"Expected {len(self._encoder)} features. Got {features.shape[1]}")

        if isinstance(features, pd.DataFrame) or isinstance(features, pd.Series):
            features = features.to_numpy()

        binarized_features = np.zeros(features.shape, dtype=self._dtype)

        for col in range(features.shape[1]):
            for row, value in enumerate(features[:, col]):
                if not self._ignore_unknown and value not in self._encoder[col]:
                    raise ValueError(f"Found new unique values which does not exist in train")
                else:
                    binarized_features[row, col] = self._encoder[col][features[row, col]]

        return binarized_features
