from sklearn.base import TransformerMixin
import pandas as pd


class BinaryEncoder(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, features):
        if isinstance(features, pd.DataFrame):
            return features.apply(lambda x: x.to_numpy(), axis="columns").to_numpy().astype(float)
        else:
            return features.astype(float)
