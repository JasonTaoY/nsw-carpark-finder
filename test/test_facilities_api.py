# tests/test_facilities_api.py

from fastapi.testclient import TestClient

from server import app
from app.core.cache import set_car_park, get_car_park
from app.core.jwt_token import create_access_token

client = TestClient(app)

set_car_park()

token = create_access_token()


async def test_get_nearby_success(monkeypatch):
    expected = {
        "487": {
            "park_name": "Park&Ride - Kogarah",
            "distance": 0
        }
    }

    def mock_distance_search(lat, lng, radius):
        assert lat == -33.96369941
        assert lng == 151.1319494
        assert radius == 1.0
        return expected

    monkeypatch.setattr("app.core.distance_search", mock_distance_search)
    car_park = get_car_park()
    await car_park.initialize_park()
    response = client.get("/carparks/nearby?lat=-33.96369941&lng=151.1319494&radius_km=1.0",
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == expected


def test_get_nearby_invalid_radius():
    response = client.get("/carparks/nearby?lat=1.0&lng=2.0&radius_km=0",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'ctx': {'gt': 0.0},
             'input': '0',
             'loc': ['query', 'radius_km'],
             'msg': 'Input should be greater than 0',
             'type': 'greater_than'}]} != {'detail': 'Radius must be greater than zero.'}


def test_get_facility_invalid_id():
    response = client.get("/carparks/abc",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid facility ID format. It should be a number."
    }


def test_get_facility_success(monkeypatch):
    expected = 259

    async def mock_facility_search(facility_id):
        assert facility_id == "487"
        return expected

    monkeypatch.setattr("app.core.facility_search", mock_facility_search)
    response = client.get("/carparks/487",
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json().get("total_spots") == expected

def teardown_module(module):
    client.close()
