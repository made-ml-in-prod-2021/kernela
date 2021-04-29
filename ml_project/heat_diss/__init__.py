import logging.config

from .log_set import LOGGER_SETUP
from .preprocessing import clean_data, feature_target_split, BinaryEncoder

logging.config.dictConfig(LOGGER_SETUP)
