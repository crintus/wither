import requests
import mock

from django.test import TestCase
from wither.open_weather_map.client import OpenWeatherMapClient


# Make a copy of this dict when using it as a mock response because the dict ID is shared
# across tests and will cause failures
MOCK_RESPONSE = {
    "lat": 33.44,
    "lon": -94.04,
    "timezone": "America/Chicago",
    "timezone_offset": -18000,
    "hourly": [
        {
            "dt": 1598158800,
            "temp": 23.19,
            "feels_like": 25.33,
            "pressure": 1015,
            "humidity": 88,
            "dew_point": 21.09,
            "clouds": 1,
            "visibility": 10000,
            "wind_speed": 2.98,
            "wind_deg": 109,
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01n"}
            ],
            "pop": 0,
        },
        {
            "dt": 1598162400,
            "temp": 22.84,
            "feels_like": 23.76,
            "pressure": 1015,
            "humidity": 78,
            "dew_point": 18.8,
            "clouds": 1,
            "visibility": 10000,
            "wind_speed": 3.18,
            "wind_deg": 134,
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01n"}
            ],
            "pop": 0,
        },
        {
            "dt": 1598166000,
            "temp": 22.22,
            "feels_like": 22.75,
            "pressure": 1014,
            "humidity": 75,
            "dew_point": 17.58,
            "clouds": 0,
            "visibility": 10000,
            "wind_speed": 2.98,
            "wind_deg": 148,
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01n"}
            ],
            "pop": 0,
        },
        {
            "dt": 1598169600,
            "temp": 22,
            "feels_like": 22.65,
            "pressure": 1014,
            "humidity": 74,
            "dew_point": 17.16,
            "clouds": 0,
            "visibility": 10000,
            "wind_speed": 2.55,
            "wind_deg": 158,
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01n"}
            ],
            "pop": 0,
        },
        {
            "dt": 1598173200,
            "temp": 21.85,
            "feels_like": 22.87,
            "pressure": 1014,
            "humidity": 75,
            "dew_point": 17.22,
            "clouds": 0,
            "visibility": 10000,
            "wind_speed": 2.06,
            "wind_deg": 164,
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01n"}
            ],
            "pop": 0,
        },
    ],
    "daily": [
        {
            "dt": 1598205600,
            "sunrise": 1598183082,
            "sunset": 1598230379,
            "temp": {
                "day": 32.88,
                "min": 20.98,
                "max": 33.97,
                "night": 23.07,
                "eve": 30.82,
                "morn": 20.98,
            },
            "feels_like": {"day": 34.48, "night": 23.85, "eve": 32.52, "morn": 23.26},
            "pressure": 1016,
            "humidity": 41,
            "dew_point": 18.21,
            "wind_speed": 1.62,
            "wind_deg": 93,
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
            ],
            "clouds": 0,
            "pop": 0,
            "uvi": 9.62,
        },
        {
            "dt": 1598292000,
            "sunrise": 1598269523,
            "sunset": 1598316706,
            "temp": {
                "day": 32.71,
                "min": 20.28,
                "max": 34.39,
                "night": 22.8,
                "eve": 30.7,
                "morn": 20.28,
            },
            "feels_like": {"day": 32.49, "night": 24.58, "eve": 31.59, "morn": 21.31},
            "pressure": 1016,
            "humidity": 37,
            "dew_point": 16.33,
            "wind_speed": 3.2,
            "wind_deg": 80,
            "weather": [
                {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
            ],
            "clouds": 0,
            "pop": 0,
            "uvi": 10.96,
        },
        {
            "dt": 1598378400,
            "sunrise": 1598355964,
            "sunset": 1598403032,
            "temp": {
                "day": 32.33,
                "min": 21.23,
                "max": 33.77,
                "night": 24.99,
                "eve": 30.26,
                "morn": 21.23,
            },
            "feels_like": {"day": 32.32, "night": 27.6, "eve": 32.35, "morn": 23.23},
            "pressure": 1015,
            "humidity": 48,
            "dew_point": 19.97,
            "wind_speed": 5.22,
            "wind_deg": 79,
            "weather": [
                {
                    "id": 802,
                    "main": "Clouds",
                    "description": "scattered clouds",
                    "icon": "03d",
                }
            ],
            "clouds": 33,
            "pop": 0.27,
            "uvi": 10.33,
        },
        {
            "dt": 1598464800,
            "sunrise": 1598442405,
            "sunset": 1598489357,
            "temp": {
                "day": 33.22,
                "min": 22.83,
                "max": 34.66,
                "night": 25.76,
                "eve": 31.79,
                "morn": 22.83,
            },
            "feels_like": {"day": 35.42, "night": 27.57, "eve": 33.54, "morn": 25.98},
            "pressure": 1011,
            "humidity": 55,
            "dew_point": 23.02,
            "wind_speed": 4.3,
            "wind_deg": 111,
            "weather": [
                {"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}
            ],
            "clouds": 31,
            "pop": 0.67,
            "rain": 1.03,
            "uvi": 9.96,
        },
        {
            "dt": 1598551200,
            "sunrise": 1598528846,
            "sunset": 1598575682,
            "temp": {
                "day": 23.02,
                "min": 21.84,
                "max": 27.26,
                "night": 21.84,
                "eve": 26.3,
                "morn": 25.7,
            },
            "feels_like": {"day": 20.67, "night": 23.93, "eve": 29.23, "morn": 26.08},
            "pressure": 1003,
            "humidity": 94,
            "dew_point": 22.08,
            "wind_speed": 10.07,
            "wind_deg": 327,
            "weather": [
                {
                    "id": 502,
                    "main": "Rain",
                    "description": "heavy intensity rain",
                    "icon": "10d",
                }
            ],
            "clouds": 100,
            "pop": 0.95,
            "rain": 44.22,
            "uvi": 10.16,
        },
    ],
}


class OpenWeatherMapClientTestCase(TestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.lat = "33.9249"
        self.lon = "18.4241"

    def test_get(self) -> None:
        wither = OpenWeatherMapClient(self.lat, self.lon)
        with mock.patch.object(requests, "get") as get:
            wither.get()
        get.assert_called_with(
            f"{wither.base_url}",
            params=dict(
                appid=OpenWeatherMapClient.api_key,
                lat=self.lat,
                lon=self.lon,
                dt=None,
                exclude="current,minutely,hourly",
                units="metric",
            ),
        )

    @mock.patch(
        "wither.open_weather_map.client.OpenWeatherMapClient._OpenWeatherMapClient__get"
    )
    def test_filter_one_day(self, mock_response) -> None:
        mock_response.return_value = MOCK_RESPONSE.copy()
        wither = OpenWeatherMapClient(self.lat, self.lon)
        self.assertDictEqual(wither.data, MOCK_RESPONSE)
        wither.filter(1598292000, 1598292000)
        self.assertEqual(len(wither.data["daily"]), 1)

    @mock.patch(
        "wither.open_weather_map.client.OpenWeatherMapClient._OpenWeatherMapClient__get"
    )
    def test_filter_from_start(self, mock_response) -> None:
        mock_response.return_value = MOCK_RESPONSE.copy()
        wither = OpenWeatherMapClient(self.lat, self.lon)
        self.assertDictEqual(wither.data, MOCK_RESPONSE)
        wither.filter(1598292000)
        self.assertEqual(len(wither.data["daily"]), 4)

    @mock.patch(
        "wither.open_weather_map.client.OpenWeatherMapClient._OpenWeatherMapClient__get"
    )
    def test_average_temp(self, mock_response) -> None:
        mock_response.return_value = MOCK_RESPONSE.copy()
        wither = OpenWeatherMapClient(self.lat, self.lon)
        wither.filter(1598205600, 1598292000)
        self.assertEqual(wither.average_temp(), 26.99)

    @mock.patch(
        "wither.open_weather_map.client.OpenWeatherMapClient._OpenWeatherMapClient__get",
    )
    def test_max_temp(self, mock_response) -> None:
        mock_response.return_value = MOCK_RESPONSE.copy()
        wither = OpenWeatherMapClient(self.lat, self.lon)
        wither.filter(1598205600, 1598292000)
        self.assertEqual(wither.max_temp(), 34.39)

    @mock.patch(
        "wither.open_weather_map.client.OpenWeatherMapClient._OpenWeatherMapClient__get",
    )
    def test_min_temp(self, mock_response) -> None:
        mock_response.return_value = MOCK_RESPONSE.copy()
        wither = OpenWeatherMapClient(self.lat, self.lon)
        wither.filter(1598205600, 1598292000)
        self.assertEqual(wither.min_temp(), 20.28)

    @mock.patch(
        "wither.open_weather_map.client.OpenWeatherMapClient._OpenWeatherMapClient__get",
    )
    def test_median_temp(self, mock_response) -> None:
        mock_response.return_value = MOCK_RESPONSE.copy()
        wither = OpenWeatherMapClient(self.lat, self.lon)
        wither.filter(1598205600, 1598292000)
        self.assertEqual(wither.median_temp(), 26.88)

    @mock.patch(
        "wither.open_weather_map.client.OpenWeatherMapClient._OpenWeatherMapClient__get",
    )
    def test_average_humidity(self, mock_response) -> None:
        mock_response.return_value = MOCK_RESPONSE.copy()
        wither = OpenWeatherMapClient(self.lat, self.lon)
        wither.filter(1598205600, 1598292000)
        self.assertEqual(wither.average_humidity(), 39.0)

    @mock.patch(
        "wither.open_weather_map.client.OpenWeatherMapClient._OpenWeatherMapClient__get",
    )
    def test_max_humidity(self, mock_response) -> None:
        mock_response.return_value = MOCK_RESPONSE.copy()
        wither = OpenWeatherMapClient(self.lat, self.lon)
        wither.filter(1598205600, 1598292000)
        self.assertEqual(wither.max_humidity(), 41)

    @mock.patch(
        "wither.open_weather_map.client.OpenWeatherMapClient._OpenWeatherMapClient__get",
    )
    def test_min_humidity(self, mock_response) -> None:
        mock_response.return_value = MOCK_RESPONSE.copy()
        wither = OpenWeatherMapClient(self.lat, self.lon)
        wither.filter(1598205600, 1598292000)
        self.assertEqual(wither.min_humidity(), 37)

    @mock.patch(
        "wither.open_weather_map.client.OpenWeatherMapClient._OpenWeatherMapClient__get",
    )
    def test_median_humidity(self, mock_response) -> None:
        mock_response.return_value = MOCK_RESPONSE.copy()
        wither = OpenWeatherMapClient(self.lat, self.lon)
        wither.filter(1598205600, 1598292000)
        self.assertEqual(wither.median_humidity(), 39.0)
