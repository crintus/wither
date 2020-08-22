import requests
from mock import patch

from django.test import TestCase
from wither.open_weather_map.client import OpenWeatherMapClient

EXAMPLE_DAILY_REPONSE = {
    "lat": 33.44,
    "lon": -94.04,
    "timezone": "America/Chicago",
    "timezone_offset": -18000,
    "daily": [
        {
            "dt": 1598119200,
            "sunrise": 1598096640,
            "sunset": 1598144051,
            "temp": {
                "day": 32.76,
                "min": 21.1,
                "max": 32.76,
                "night": 22.88,
                "eve": 28.67,
                "morn": 21.1,
            },
            "feels_like": {"day": 34.88, "night": 23.73, "eve": 30.35, "morn": 23.25},
            "pressure": 1013,
            "humidity": 43,
            "dew_point": 18.54,
            "wind_speed": 1.28,
            "wind_deg": 62,
            "weather": [
                {
                    "id": 802,
                    "main": "Clouds",
                    "description": "scattered clouds",
                    "icon": "03d",
                }
            ],
            "clouds": 33,
            "pop": 0,
            "uvi": 9.22,
        },
        {
            "dt": 1598205600,
            "sunrise": 1598183082,
            "sunset": 1598230379,
            "temp": {
                "day": 33.12,
                "min": 20.85,
                "max": 33.12,
                "night": 23.37,
                "eve": 30.45,
                "morn": 20.85,
            },
            "feels_like": {"day": 35.03, "night": 24.45, "eve": 32.92, "morn": 22.79},
            "pressure": 1016,
            "humidity": 42,
            "dew_point": 18.58,
            "wind_speed": 1.55,
            "wind_deg": 110,
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
            ],
            "clouds": 0,
            "pop": 0,
            "uvi": 10.02,
        },
        {
            "dt": 1598292000,
            "sunrise": 1598269523,
            "sunset": 1598316706,
            "temp": {
                "day": 32.7,
                "min": 20.54,
                "max": 34.31,
                "night": 24.01,
                "eve": 31.08,
                "morn": 20.54,
            },
            "feels_like": {"day": 32.99, "night": 26.15, "eve": 33.06, "morn": 21.65},
            "pressure": 1017,
            "humidity": 40,
            "dew_point": 17.71,
            "wind_speed": 3.17,
            "wind_deg": 89,
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
            ],
            "clouds": 0,
            "pop": 0,
            "uvi": 10.3,
        },
        {
            "dt": 1598378400,
            "sunrise": 1598355964,
            "sunset": 1598403032,
            "temp": {
                "day": 32.2,
                "min": 22.31,
                "max": 34.46,
                "night": 23.89,
                "eve": 31.01,
                "morn": 22.31,
            },
            "feels_like": {"day": 33.87, "night": 27.34, "eve": 33.9, "morn": 24.84},
            "pressure": 1016,
            "humidity": 51,
            "dew_point": 21.09,
            "wind_speed": 3.42,
            "wind_deg": 90,
            "weather": [
                {"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}
            ],
            "clouds": 13,
            "pop": 0.88,
            "rain": 0.84,
            "uvi": 10.95,
        },
        {
            "dt": 1598464800,
            "sunrise": 1598442405,
            "sunset": 1598489357,
            "temp": {
                "day": 32.16,
                "min": 23.55,
                "max": 35.3,
                "night": 25.13,
                "eve": 31.97,
                "morn": 23.55,
            },
            "feels_like": {"day": 34.03, "night": 27.88, "eve": 33.44, "morn": 26.42},
            "pressure": 1013,
            "humidity": 59,
            "dew_point": 23.19,
            "wind_speed": 4.91,
            "wind_deg": 113,
            "weather": [
                {
                    "id": 501,
                    "main": "Rain",
                    "description": "moderate rain",
                    "icon": "10d",
                }
            ],
            "clouds": 59,
            "pop": 0.75,
            "rain": 3.64,
            "uvi": 10.13,
        },
        {
            "dt": 1598551200,
            "sunrise": 1598528846,
            "sunset": 1598575682,
            "temp": {
                "day": 25.88,
                "min": 22.91,
                "max": 26.82,
                "night": 22.98,
                "eve": 22.91,
                "morn": 23.54,
            },
            "feels_like": {"day": 27.54, "night": 21.4, "eve": 19.49, "morn": 25.69},
            "pressure": 1010,
            "humidity": 83,
            "dew_point": 22.9,
            "wind_speed": 4.93,
            "wind_deg": 103,
            "weather": [
                {
                    "id": 503,
                    "main": "Rain",
                    "description": "very heavy rain",
                    "icon": "10d",
                }
            ],
            "clouds": 100,
            "pop": 1,
            "rain": 81.94,
            "uvi": 9.8,
        },
        {
            "dt": 1598637600,
            "sunrise": 1598615287,
            "sunset": 1598662006,
            "temp": {
                "day": 29.94,
                "min": 22.04,
                "max": 31.91,
                "night": 22.86,
                "eve": 28.46,
                "morn": 22.04,
            },
            "feels_like": {"day": 29.51, "night": 25.25, "eve": 30.56, "morn": 21.65},
            "pressure": 1010,
            "humidity": 58,
            "dew_point": 20.91,
            "wind_speed": 6.42,
            "wind_deg": 261,
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
            ],
            "clouds": 2,
            "pop": 0.15,
            "uvi": 9.47,
        },
        {
            "dt": 1598724000,
            "sunrise": 1598701728,
            "sunset": 1598748329,
            "temp": {
                "day": 31.47,
                "min": 21.55,
                "max": 33.85,
                "night": 29.68,
                "eve": 29.68,
                "morn": 21.55,
            },
            "feels_like": {"day": 33.65, "night": 32.7, "eve": 32.7, "morn": 23.43},
            "pressure": 1013,
            "humidity": 51,
            "dew_point": 20.37,
            "wind_speed": 2.23,
            "wind_deg": 359,
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
            ],
            "clouds": 0,
            "pop": 0,
            "uvi": 9.35,
        },
    ],
}


class OpenWeatherMapClientTestCase(TestCase):
    def setUp(self) -> None:
        self.lat = "33.9249"
        self.lon = "18.4241"
        self.wither = OpenWeatherMapClient(self.lat, self.lon)

    def test_get(self) -> None:
        with patch.object(requests, "get") as get:
            self.wither.get()
        get.assert_called_with(
            f"{self.wither.base_url}",
            params=dict(
                appid=OpenWeatherMapClient.api_key,
                lat=self.lat,
                lon=self.lon,
                dt=None,
                exclude="current,minutely,hourly",
            ),
        )
