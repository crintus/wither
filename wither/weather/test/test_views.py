import mock
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

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


class TestWeatherViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("weather-list")

    @mock.patch(
        "wither.open_weather_map.client.OpenWeatherMapClient.get",
        side_effect=lambda: MOCK_RESPONSE,
    )
    def test_list(self, *args, **kwargs) -> None:
        response = self.client.get(self.url, dict(location="Cape Town"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MOCK_RESPONSE)

    def test_list_location_not_provided(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, ["The location query paramater is required."])


class TestWeatherSummaryViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("weather-summary-list")

    def test_list_location_not_provided(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, ["The location query paramater is required."])

    def test_list_invalid_location(self) -> None:
        response = self.client.get(self.url, dict(location="qqqqq"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, ["Invalid location."])

    @mock.patch("wither.open_weather_map.client.OpenWeatherMapClient.get",)
    def test_list_without_period_set(self, mock_response) -> None:
        mock_response.return_value = MOCK_RESPONSE.copy()
        response = self.client.get(self.url, dict(location="Cape Town"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: assert response data
