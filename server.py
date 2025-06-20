from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.router_factory import api_router
from app import logger
import uvicorn

from app.core.cache import set_car_park, set_scheduler, get_scheduler, get_car_park

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Car Park API initialized with global variables and scheduler running.")
    set_car_park()
    set_scheduler()
    car_park = get_car_park()
    await car_park.initialize_park()
    scheduler = get_scheduler()
    scheduler.scheduler.start()

    logger.info("Car Park API is ready to handle requests.")
    yield
    scheduler.scheduler.shutdown()
    logger.info("Car Park API shutdown complete.")

app = FastAPI(
    title="Car Park API",
    version="0.0.1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


