import os
import json
import logging

import hydra
from hydra.core.config_store import ConfigStore
from sklearn import compose, pipeline
from sklearn import model_selection
import pandas as pd
import numpy as np

from heat_diss.preprocessing import feature_target_split, clean_data
from config import CrossValConfig, \
    FeatureTransformerConfig, TrainConfig, \
    LogisticRegressionConfig, SVCConfig
from utils import get_class_type

cs = ConfigStore().instance()
cs.store(group="cls_config", name="svc", node=SVCConfig)
cs.store(group="cls_config", name="log_reg", node=LogisticRegressionConfig)
cs.store(name="feature_transform", node=FeatureTransformerConfig)
cs.store(name="cross_val", node=CrossValConfig)
cs.store(name="train", node=TrainConfig)


def prepare_date(path_to_zip: str, uniq_values_limit: int, target_variable: str):
    data = pd.read_csv(path_to_zip)
    data = clean_data(data, uniq_values_limit)
    return feature_target_split(data, target_variable)


@hydra.main(config_name="train")
def train(cfg: TrainConfig):
    logger = logging.getLogger()
    column_transformers = compose.ColumnTransformer([(transform.stage_name,
                                                      get_class_type(transform.classname)(**transform.params), pd.Index(transform.columns))
                                                     for transform in cfg.feature_transform.transformers], remainder="drop")
    cls_params = dict(cfg.cls_config)
    cls_params.pop("classname")
    cls = get_class_type(cfg.cls_config.classname)(**cls_params)

    cls_pipeline = pipeline.Pipeline([
        ("feature_transform", column_transformers),
        ("cls", cls)
    ])

    features, target = prepare_date(os.path.join(hydra.utils.get_original_cwd(), cfg.data_config.input_data),
                                    cfg.data_config.unique_values_limit, cfg.data_config.target_variable)

    cross_val_score = model_selection.cross_validate(cls_pipeline, features, target,
                                                     scoring=list(cfg.cross_val.scores),
                                                     cv=cfg.cross_val.cv)

    for score in cross_val_score:
        if isinstance(cross_val_score[score], np.ndarray):
            cross_val_score[score] = list(cross_val_score[score])

    metric_path = os.path.join(hydra.utils.get_original_cwd(), cfg.output_metric)

    logger.info("Save metrics to %s", metric_path)

    os.makedirs(os.path.dirname(metric_path), exist_ok=True)

    with open(metric_path, "w", encoding="utf-8") as file:
        json.dump(cross_val_score, file, )


if __name__ == "__main__":
    train()
