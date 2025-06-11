from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.cache.location import CarPark


class CarParkScheduler:
    def __init__(self, car_park: CarPark):
        self.car_park = car_park
        self.scheduler = AsyncIOScheduler()

        self.scheduler.add_job(
            func=self.car_park.initialize_park,
            trigger=CronTrigger(day_of_week='mon', hour=0, minute=0),
        )
