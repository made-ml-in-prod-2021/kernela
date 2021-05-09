from fastapi import FastAPI

from .api import predict_router
from .config import AppConfig

config = AppConfig()

app = FastAPI(debug=config.debug, title=config.app_name, version=config.app_version)

app.include_router(predict_router)
