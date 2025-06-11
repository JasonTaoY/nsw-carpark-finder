import asyncio
from datetime import datetime
import aiohttp
from fastapi import HTTPException

from app.config import config
from math import radians, sin, cos, sqrt, pow, asin

rad = 6371.0

class RateLimitError(Exception):
    """Custom exception for rate limiting errors."""
    pass

async def fetch_url(url: str, timeout : float = 3.0) -> dict:
    """
    Fetch data from a given URL with optional headers.
    :param timeout: The timeout for the request in seconds.
    :param url: The URL to fetch data from.
    :param headers: Optional headers for the request.
    :return: Parsed JSON response as a dictionary.
    """
    timeout = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=config.headers) as response:
            if response.status == 429:
                text = await response.text()
                raise RateLimitError(f"Rate limit exceeded: {text}")
            if response.status == 404:
                raise HTTPException(status_code=404, detail="Facility Not found.")
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Error fetching data: {response.status} - {await response.text()}")

async def fetch_with_retry(url: str, retries: int = 3, delay: float = 1.0,timeout: float = 3.0) -> dict:
    """
    Try up to `retries` times on RateLimitError, with exponential back-off.
    """
    for attempt in range(1, retries + 1):
        try:
            return await fetch_url(url,timeout)
        except RateLimitError:
            if attempt == retries:
                raise
            await asyncio.sleep(delay * 2 * (attempt - 1))
        except Exception:
            raise
    return {}


def formatted_facility_search(facility_metadata: dict) -> dict:
    """
    Format the facility metadata into a more readable structure.
    :param facility_metadata:
    :return:
    Dictionary containing formatted facility details.
    """
    spots = int(facility_metadata.get("spots", 0))
    occupied = int(facility_metadata.get("occupancy", {"total": 0}).get("total", 0))
    available = spots - occupied
    # Determine the status based on available spots
    if available < 1:
        status = "Full"
    elif available / spots < 0.10:
        status = "Almost Full"
    else:
        status = "Available"

    # Convert date string to datetime object
    iso_str = facility_metadata.get("MessageDate")
    dt = datetime.fromisoformat(iso_str)

    return {
        "total_spots": spots,
        "available_spots": available,
        "status": status,
        "timestamp":int(dt.timestamp())
    }

def calc_distance(lat1: float, lng1: float, lat2, lng2) -> float:
    """
    Calculate the distance between two geographical points using the Haversine formula.
    Details from https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
    :param lat1: Latitude of the first point.
    :param lng1: Longitude of the first point.
    :param lat2: Latitude of the second point.
    :param lng2: Longitude of the second point.
    :return: Distance in kilometers.
    """

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    lat_dist = radians(lat2) - radians(lat1)
    lng_dist = radians(lng2) - radians(lng1)

    # Haversine formula:
    a = pow(sin(lat_dist / 2), 2) + pow(sin(lng_dist / 2), 2) * cos(lat1_rad) * cos(lat2_rad)
    # Radius of the Earth in kilometers (mean radius)
    c = 2 * asin(sqrt(a))
    return rad * c



