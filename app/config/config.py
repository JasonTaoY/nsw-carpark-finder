import os
from unittest.mock import DEFAULT

import dotenv

dotenv.load_dotenv()

DEFAULTS = {
    "CAR_PARK_API": "",
    "NSW_TRANSPORT_URL":"",
    "HISTORICAL_MARKER": "historical only",
    "JWT_SECRET_KEY":"default_secret_key",

}

def get_env_variable(var_name, default_value=None):
    """
    Get the environment variable or return the default value.
    """
    return os.environ.get(var_name, DEFAULTS.get(var_name, default_value))

class Config:
    def __init__(self):
        self.car_park_api = get_env_variable("CAR_PARK_API")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"apikey {self.car_park_api}",
        }
        self.historical_marker = get_env_variable("HISTORICAL_MARKER")
        self.nsw_transport_url = get_env_variable("NSW_TRANSPORT_URL")
        self.jwt_secret_key = get_env_variable("JWT_SECRET_KEY")

config = Config()