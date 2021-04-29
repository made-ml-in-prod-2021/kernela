import pandas as pd
from sklearn import compose
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from .transformer import BinaryEncoder


def clean_data(data: pd.DataFrame, category_threshold: int):
    filtered_data = data.copy().drop_duplicates()

    for col in filtered_data.columns:
        if len(filtered_data[col].unique()) <= category_threshold:
            filtered_data[col] = filtered_data[col].astype("category")

    return filtered_data


def feature_target_split(data: pd.DataFrame, target_variable: str):
    return data[data.columns.drop(target_variable)].copy(), data[target_variable].to_numpy()


def get_numeric_transform(col_names, **kwargs):
    return compose.ColumnTransformer([("normalize", StandardScaler(**kwargs), col_names)])


def get_categorical_transfomer(col_names, **kwargs):
    return compose.ColumnTransformer([("cat_encoder", OneHotEncoder(**kwargs), col_names)])


def get_binary_transfomer(col_names, **kwargs):
    return compose.ColumnTransformer([("bin_encoder", BinaryEncoder(**kwargs), col_names)])
