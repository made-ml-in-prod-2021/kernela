import pathlib
import logging

import pandas as pd
import hydra
from hydra.core.config_store import ConfigStore

from heat_diss.preprocessing import feature_target_split
from config import PredictConfig, TrainConfig, TrainTestSplitConfig

from utils import load_dump


cs = ConfigStore().instance()
cs.store(group="split", name="train_test_split", node=TrainTestSplitConfig)
cs.store(group="train", name="train", node=TrainConfig)
cs.store(name="predict", node=PredictConfig)


@hydra.main(config_name="predict")
def main(cfg: PredictConfig):
    logger = logging.getLogger()

    orig_wd = pathlib.Path(hydra.utils.get_original_cwd())
    model_path = orig_wd / cfg.train.model_path

    logger.info("Load model from %s", model_path)

    model = load_dump(str(model_path))

    test_data = pd.read_csv(orig_wd / cfg.train_test_split.out_path_test)

    test_features, _ = feature_target_split(test_data,
                                            cfg.train.data_config.target_variable)

    predicted_classes = model.predict(test_features)

    out_pred = orig_wd / cfg.out_prediction
    out_pred.parent.mkdir(exist_ok=True, parents=True)

    logger.info("Save predictions to %s", out_pred)

    test_data["predicted"] = predicted_classes
    test_data.to_csv(out_pred, index=False)


if __name__ == "__main__":
    main()
