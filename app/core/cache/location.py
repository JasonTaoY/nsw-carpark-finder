import asyncio

from fastapi.background import BackgroundTasks
from aiolimiter import AsyncLimiter
from app.config import config
from app.core.utils import fetch_url


class CarPark:
    def __init__(self):
        self.park = {}
        self.location = {}
        self._limiter = AsyncLimiter(5, 1)
        self._sem = asyncio.Semaphore(2)

    async def fetch_car_park(self):
        """
        Fetch car park data from the API.
        """
        data = await fetch_url(config.nsw_transport_url)
        self.park = {key: value for key, value in data.items() if config.historical_marker not in value}

    async def fetch_location(self,facility_id: str):
        """
        Fetch location data for a specific facility.
        :param facility_id: The ID of the facility to fetch.
        """
        async with self._sem, self._limiter:
            url = f"{config.nsw_transport_url}?facility={facility_id}"
            data = await fetch_url(url)
            location = data.get("location",None)
            if location and isinstance(location, dict):
                lat = float(location.get("latitude"))
                lng = float(location.get("longitude"))
                self.location[(lat, lng)] = facility_id
            else:
                raise ValueError(f"Location data not found for facility ID: {facility_id}")

    async def initialize_park(self):
        """
        Initialize the car park data.
        This method can be extended to load initial data or set up periodic updates.
        """
        await self.fetch_car_park()
        facility_ids = list(self.park.keys())
        tasks = [self.fetch_location(facility_id) for facility_id in facility_ids]
        await asyncio.gather(*tasks)








