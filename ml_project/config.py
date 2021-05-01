from dataclasses import dataclass
from typing import Any, List

from omegaconf import MISSING


@dataclass
class ReportConfig:
    input_zip: str = MISSING
    output_report: str = MISSING


@dataclass
class TrainTestSplitConfig:
    target_variable: str = MISSING
    train_size: float = MISSING
    path_zip: str = MISSING
    out_path_train: str = MISSING
    out_path_test: str = MISSING
    random_state: int = MISSING


@dataclass
class CrossValConfig:
    cv: int = MISSING
    conf_matrix_metric_path: str = MISSING
    cross_val_method: str = MISSING


@dataclass
class TransformerConfig:
    classname: str = MISSING
    columns: List[str] = MISSING
    params: Any = MISSING
    stage_name: str = MISSING


@dataclass
class ClsConfog:
    classname: str = MISSING
    params: Any = MISSING


@dataclass
class FeatureTransformerConfig:
    transformers: List[TransformerConfig] = MISSING


@dataclass
class DataConfig:
    path_to_train: str = MISSING
    path_to_test: str = MISSING
    target_variable: str = MISSING
    unique_values_limit: int = MISSING


@dataclass
class TrainConfig:
    model_path: str = MISSING
    cls_config: ClsConfog = MISSING
    cross_val: CrossValConfig = MISSING
    feature_transform: FeatureTransformerConfig = MISSING
    data_config: DataConfig = MISSING
    output_metric: str = MISSING


@dataclass
class PredictConfig:
    train_test_split: TrainTestSplitConfig = MISSING
    train: TrainConfig = MISSING
    out_prediction: str = MISSING


@dataclass
class PlotConfMatrixConfig:
    train: TrainConfig = MISSING
    output_image: str = MISSING
    actual_col: str = MISSING
    predicted_col: str = MISSING
    normalize: str = MISSING
    cmap: str = "summer_r"
    interpolation: str = "none"
    title: str = "Cross validation confusion matrix"
    fromat_str: str = "{0:.4f}"
    dpi: int = 300
    width_inches: int = 3
    height_inches: int = 3
