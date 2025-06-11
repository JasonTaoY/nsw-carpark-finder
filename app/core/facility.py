import asyncio
from fastapi.concurrency import run_in_threadpool
from app.config import config
from .utils import calc_distance, fetch_with_retry, formatted_facility_search
from app.core.cache import get_car_park


async def facility_search(facility_id:str) -> dict:
    """
    Search for facilities based on facility ID.
    :param facility_id:
    :return: Dictionary containing facility details.
    """

    url = f"{config.nsw_transport_url}?facility={facility_id}"
    data = await fetch_with_retry(url)
    return formatted_facility_search(data)

async def distance_search(lat: float, lng: float, radius_km: float) -> dict:
    """
    Search for facilities within a specified radius from a given latitude and longitude.
    :param lat: Latitude of the center point.
    :param lng: Longitude of the center point.
    :param radius_km: Radius in kilometers to search within.
    :return: Dictionary containing facility IDs and their distances from the center point.
    """
    car_park = get_car_park()
    park = car_park.park
    location = car_park.location

    tasks = [run_in_threadpool(calc_distance,lat, lng, lat2, lng2) for (lat2, lng2), facility_id in location.items()]
    distances = await asyncio.gather(*tasks)
    facility_distances = {facility_id: distance for facility_id, distance in zip(location.values(), distances) if distance <= radius_km}
    sorted_facility_distances = sorted(facility_distances.items(), key=lambda item: item[1],reverse=True)

    nearby_facilities = {facility_id: {"park_name":park[facility_id],"distance":distance} for facility_id, distance in sorted_facility_distances}
    for facility_id in nearby_facilities.keys():
        if facility_id not in park:
            raise ValueError(f"Facility ID {facility_id} not found in the park data.")

    return nearby_facilities



