from typing import List

from fastapi import APIRouter, Request, Depends

from ..models import Prediction, Features
from ..predictor import HeartDissPredictor

predict_router = APIRouter()


def get_model(request: Request):
    return request.state.model


@predict_router.post("/predict", response_model=List[Prediction])
async def predict(features: Features, model: HeartDissPredictor = Depends(get_model)):
    return model.predict(features)
