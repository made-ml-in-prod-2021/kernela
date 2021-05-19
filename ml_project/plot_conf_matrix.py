import pathlib
import logging

import pandas as pd
import hydra
from hydra.core.config_store import ConfigStore
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt

from config import PlotConfMatrixConfig, TrainConfig


cs = ConfigStore().instance()
cs.store(name="plot_conf_matrix", node=PlotConfMatrixConfig)
cs.store(name="train", node=TrainConfig)


@hydra.main(config_name="plot_conf_matrix")
def plot(cfg: PlotConfMatrixConfig):
    logger = logging.getLogger()

    orig_wd = pathlib.Path(hydra.utils.get_original_cwd())
    data_path = orig_wd / cfg.train.cross_val.conf_matrix_metric_path

    logger.info("Load predcitions from %s", data_path)

    data = pd.read_csv(data_path)

    conf_matrix = confusion_matrix(
        data[cfg.actual_col], data[cfg.predicted_col], normalize=cfg.normalize)

    fig = plt.figure(figsize=(cfg.width_inches, cfg.height_inches))
    ax = fig.add_subplot(111)
    ax.set_title(cfg.title)
    ax.imshow(conf_matrix, interpolation=cfg.interpolation, cmap=cfg.cmap)
    uniq_labels = len(data[cfg.actual_col].unique())
    labels = tuple(range(uniq_labels))

    ax.set_xticks(labels)
    ax.set_yticks(labels)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

    for i in labels:
        for j in labels:
            text = ax.text(j, i, cfg.fromat_str.format(conf_matrix[i, j]),
                           ha="center", va="center", color="black")

    logger.info("Save image to %s", cfg.output_image)
    fig.savefig(str(orig_wd / cfg.output_image), bbox_inches="tight", dpi=cfg.dpi)


if __name__ == "__main__":
    plot()
