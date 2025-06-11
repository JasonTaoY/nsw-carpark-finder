import asyncio

from app.core.cache.location import CarPark
from app.core.cache.tasks import CarParkScheduler

global car_park
global scheduler

def set_car_park():
    global car_park
    car_park = CarPark()

def set_scheduler():
    global scheduler
    global car_park
    scheduler = CarParkScheduler(car_park)

def get_car_park():
    global car_park
    if car_park is None:
        raise ValueError("Car park data has not been initialized. Call initialize_globals() first.")
    return car_park

def get_scheduler():
    global scheduler
    if scheduler is None:
        raise ValueError("Scheduler has not been initialized. Call run_scheduler() first.")
    return scheduler

