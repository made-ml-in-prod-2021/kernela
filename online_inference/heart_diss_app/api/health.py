from typing import List

from fastapi import APIRouter, Request, Depends


health_router = APIRouter()


@health_router.get("/health")
async def health():
    return {"status": "OK"}
