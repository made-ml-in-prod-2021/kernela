from typing import List

from fastapi import APIRouter

from ..models import Prediction, Indicators

predict_router = APIRouter()


@predict_router.post("/predict/", response_model=Prediction)
async def predict(indicators: List[Indicators]):
    return Prediction(heart_disease=True)
