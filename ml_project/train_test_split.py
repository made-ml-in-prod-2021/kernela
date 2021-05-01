import pathlib
import logging

import pandas as pd
import hydra
from sklearn import model_selection

import heat_diss
from config import TrainTestSplitConfig


@hydra.main(config_name="train_test_split")
def main(config: TrainTestSplitConfig):
    orig_wd = pathlib.Path(hydra.utils.get_original_cwd())
    logger = logging.getLogger()
    zip_file = orig_wd / config.path_zip

    data = pd.read_csv(zip_file)

    x_train, x_test = model_selection.train_test_split(
        data, train_size=config.train_size, random_state=config.random_state)

    logger.info("Train distr:\n%s", x_train[config.target_variable].value_counts(normalize=True))
    logger.info("Test distr:\n%s", x_test[config.target_variable].value_counts(normalize=True))

    logger.info("Train size: %s", x_train.shape)
    logger.info("Test size: %s", x_test.shape)

    out_train = orig_wd / config.out_path_train
    out_train.parent.mkdir(exist_ok=True, parents=True)

    logger.info("Save train to %s", out_train.parent)
    x_train.to_csv(out_train, index=False)

    out_test = orig_wd / config.out_path_test
    out_test.parent.mkdir(exist_ok=True, parents=True)

    logger.info("Save test to %s", out_test.parent)
    x_train.to_csv(out_test, index=False)


if __name__ == "__main__":
    main()
