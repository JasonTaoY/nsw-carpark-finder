# NSW Car Park Finder

A FastAPI-based REST API service that provides real-time car park availability information for New South Wales (NSW) transport facilities. The service integrates with the NSW Transport Open Data API to deliver up-to-date parking information with location-based search capabilities.

## Features

- **Location-based Search**: Find nearby car parks within a specified radius
- **Real-time Data**: Get current availability, occupancy, and status information
- **Rate Limiting**: Built-in protection against API abuse
- **Automated Data Updates**: Scheduled background tasks to keep data fresh
- **Docker Deployment**: Production-ready containerized deployment with nginx
- **Distance Calculation**: Haversine formula implementation for accurate distance measurements

## API Endpoints

### Get Nearby Car Parks
```http
GET /carparks/nearby?lat={latitude}&lng={longitude}&radius_km={radius}
```

**Parameters:**
- `lat`: Your latitude coordinate
- `lng`: Your longitude coordinate  
- `radius_km`: Search radius in kilometers (must be > 0)

**Response:**
```json
{
  "487": {
    "park_name": "Park&Ride - Kogarah",
    "distance": 0.8
  }
}
```

### Get Specific Car Park Details
```http
GET /carparks/{facility_id}
```

**Response:**
```json
{
  "total_spots": 259,
  "available_spots": 45,
  "status": "Available",
  "timestamp": 1749701607
}
```

**Status Values:**
- `Available`: More than 10% of spots available
- `Almost Full`: Less than 10% of spots available
- `Full`: No spots available

## Authentication

All API endpoints require JWT authentication. Include the token in the Authorization header:

```http
Authorization: Bearer {your_jwt_token}
```
Check the notebook for how to generate a JWT token.
## Setup & Installation

### Prerequisites

- Python 3.10+
- NSW Transport API key (from [NSW Open Data](https://opendata.transport.nsw.gov.au/))

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/nsw-carpark-finder.git
cd nsw-carpark-finder
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration:**
```bash
cp .env.example .env
```

4. **Run the application:**
```bash
python server.py
```

The API will be available at `http://localhost:8000`

### Docker Deployment

For production deployment using Docker:

```bash
cd deploy/prod
docker-compose -f docker-compose.prod.yaml up -d
```

This will start:
- FastAPI application on port 8000
- Nginx proxy with SSL on port 443


### Rate Limiting

- API requests: 5 requests per second
- Concurrent requests: Limited by semaphore (5 concurrent)
- Retry logic: 3 attempts with exponential backoff

## Data Updates

The application automatically refreshes car park data:
- **Initial Load**: On application startup
- **Scheduled Updates**: Every Monday at midnight (configurable via cron)
- **Rate Limited**: API calls are throttled to respect NSW Transport API limits

## Testing

Run the test suite:

```bash
pytest
```

## Deployment

### CI/CD Pipeline

The project includes GitHub Actions workflows for:
- Automated testing on push/PR
- Deployment to EC2 on successful tests

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## API Documentation

Once running, interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment
Now deployed on AWS EC2 with Nginx reverse proxy and SSL termination.
- URL: [https://16.176.204.96/]

## Acknowledgments

- NSW Transport for providing the Open Data API
- FastAPI community for the excellent framework
- Contributors and maintainers