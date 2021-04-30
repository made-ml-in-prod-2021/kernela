from dataclasses import dataclass
from typing import Any, List
from enum import Enum, auto

from omegaconf import MISSING


class FeatureType(Enum):
    BINARY = auto()
    CATEGORICAL = auto()
    NUMERIC = auto()


@dataclass
class ReportConfig:
    input_zip: str = MISSING
    output_report: str = MISSING


@dataclass
class TrainTestSplitConfig:
    target_variable: str = MISSING
    train_size: float = MISSING
    path_zip: str = MISSING
    out_dir: str = MISSING
    random_state: int = MISSING


@dataclass
class CrossValConfig:
    random_state: int = MISSING
    cv: int = MISSING
    scores: List[str] = MISSING
    refit_score: str = MISSING


@dataclass
class TransformerConfig:
    classname: str = MISSING
    columns: List[str] = MISSING
    params: Any = MISSING
    stage_name: str = MISSING


@dataclass
class ClsConfog:
    classname: str = MISSING


@dataclass
class LogisticRegressionConfig(ClsConfog):
    C: float = MISSING
    max_iter: int = MISSING


@dataclass
class SVCConfig(ClsConfog):
    C: float = MISSING
    max_iter: int = MISSING


@dataclass
class FeatureTransformerConfig:
    transformers: List[TransformerConfig] = MISSING


@dataclass
class DataConfig:
    input_data: str = MISSING
    target_variable: str = MISSING
    unique_values_limit: int = MISSING


@dataclass
class TrainConfig:
    cls_config: ClsConfog = MISSING
    feature_transform: FeatureTransformerConfig = MISSING
    data_config: DataConfig = MISSING
    output_metric: str = MISSING
