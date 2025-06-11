# app/api/router_factory.py
from fastapi import APIRouter
from .endpoints import car_park_router


api_router = APIRouter()

api_router.include_router(
    car_park_router,
    prefix="/carparks",
    tags=["carparks"]
)
