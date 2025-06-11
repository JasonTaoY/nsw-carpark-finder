import asyncio
from typing import Dict
from fastapi import APIRouter, HTTPException
from fastapi.params import Query

from app.core import distance_search, facility_search
from aiolimiter import AsyncLimiter

from app.core.utils import RateLimitError

router = APIRouter()
_limiter = AsyncLimiter(5, 1)

_semaphore = asyncio.Semaphore(5)

@router.get("/nearby")
async def get_nearby(
        lat: float = Query(..., description="Your latitude"),
        lng: float = Query(..., description="Your longitude"),
        radius_km: float = Query(..., gt=0, description="Search radius in km"),
) -> Dict:
    """
    Get nearby facilities within a specified radius from a given latitude and longitude.
    :param lat: Latitude of the center point.
    :param lng: Longitude of the center point.
    :param radius_km: Radius in kilometers to search within.
    :return: Dictionary containing facility IDs and their distances from the center point.
    """
    return await distance_search(lat, lng, radius_km)


@router.get("/{facility_id}")
async def get_facility(facility_id: str) -> Dict:
    """
    Get details of a specific facility by its ID.
    :param facility_id: The ID of the facility to fetch.
    :return: Dictionary containing formatted facility details.
    """
    try:
        int(facility_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid facility ID format. It should be a number.")
    async with _semaphore, _limiter:
        try:
            return await facility_search(facility_id)
        except RateLimitError:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")





