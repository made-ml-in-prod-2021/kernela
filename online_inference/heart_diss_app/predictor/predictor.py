import pathlib
from typing import Union, List

import pandas as pd

from ..utils import load_pickle
from ..models import Features, Prediction


class HeartDissPredictor:
    def __init__(self, path_to_pipeline: Union[str, pathlib.Path]):
        self._model = load_pickle(path_to_pipeline)

    def predict(self, entities: Features) -> List[Prediction]:
        features_data = pd.DataFrame.from_records([entity.dict() for entity in entities.features])
        return [Prediction(heart_disease=prediction) for prediction in self._model.predict(features_data)]
