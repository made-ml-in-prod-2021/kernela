from typing import List
from pydantic import BaseSettings


class AppConfig(BaseSettings):
    app_name: str = "Heart Disease Prediction"
    debug: bool = True
    app_version: str = "0.0.1"
