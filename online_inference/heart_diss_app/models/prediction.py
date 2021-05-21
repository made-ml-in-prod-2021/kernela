from pydantic import BaseModel
from pydantic.fields import Field


class Prediction(BaseModel):
    heart_disease: int = Field(example=True, ge=0, le=1,
                               description="1 if heart disease detected otherwise 0")
