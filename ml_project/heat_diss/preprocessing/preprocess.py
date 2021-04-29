import pandas as pd


def clean_data(data: pd.DataFrame, category_threshold: int):
    filtered_data = data.copy().drop_duplicates()

    for col in filtered_data.columns:
        if len(filtered_data[col].unique()) <= category_threshold:
            filtered_data[col] = filtered_data[col].astype("category")

    return filtered_data


def feature_target_split(data: pd.DataFrame, target_variable: str):
    return data[data.columns.drop(target_variable)].copy(), data[target_variable].to_numpy()
