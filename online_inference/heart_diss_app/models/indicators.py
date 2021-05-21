from typing import List
from pydantic import BaseModel, conint, confloat, Field


class Indicators(BaseModel):
    age: conint(gt=0, lt=150, strict=True)
    sex: conint(ge=0, le=1, strict=True)
    cp: conint(ge=0, le=3, strict=True)
    trestbps: confloat(gt=0)
    chol: confloat(gt=0)
    fbs: conint(ge=0, le=1, strict=True)
    restecg: conint(ge=0, le=2, strict=True)
    thalach: confloat(gt=0)
    exang: conint(ge=0, le=1, strict=True)
    oldpeak: confloat()
    slope: conint(ge=0, le=2, strict=True)
    ca: conint(ge=0, le=4, strict=True)
    thal: conint(ge=0, le=3, strict=True)

    class Config:
        schema_extra = {
            "example": {
                "age": 25,
                "sex": 0,
                "cp": 3,
                "trestbps": 150.0,
                "chol": 226.0,
                "fbs": 0,
                "restecg": 1,
                "thalach": 114.0,
                "exang": 1,
                "oldpeak": 2.6,
                "slope": 2,
                "ca": 2,
                "thal": 2
            }
        }


class Features(BaseModel):
    features: List[Indicators] = Field(min_items=1)
