from pydantic import BaseModel
from pydantic.fields import Field


class Prediction(BaseModel):
    heart_disease: bool = Field(example=True)
