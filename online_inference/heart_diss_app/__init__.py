import os

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError

from .api import predict_router
from .config import AppConfig
from .predictor import HeartDissPredictor


config_app = AppConfig()
app = FastAPI(debug=config_app.debug, title=config_app.app_name, version=config_app.app_version)

if not os.path.isfile(config_app.model_path):
    raise RuntimeError(f"'{config_app.model_path}' is not a file")

model = HeartDissPredictor(config_app.model_path)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.middleware("http")
async def add_model(request: Request, call_next):
    request.state.model = model
    response = await call_next(request)
    return response

app.include_router(predict_router)
