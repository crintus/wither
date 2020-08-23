from typing import Dict

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import ValidationError

from wither.open_weather_map.client import OpenWeatherMapClient
from wither.utils import latitude_longitude_from_location


class WeatherViewSet(ViewSet):
    """
    Returns the raw weather data
    """

    permission_classes = (permissions.AllowAny,)

    def validate_query_params(self, params: Dict) -> None:
        """Validated the query params

        Args:
            params (dict): query params

        Raises:
            ValidationError: If the params are invalid
        """
        if not params.get("location"):
            raise ValidationError("The location query paramater is required.")

    def list(self, request):
        self.validate_query_params(request.query_params)

        try:
            lat, lon = latitude_longitude_from_location(
                request.query_params.get("location")
            )
        except AttributeError:
            raise ValidationError("Invalid location.")

        weather_client = OpenWeatherMapClient(lat, lon)
        return Response(weather_client.get(), status=200,)


class WeatherSummaryViewSet(ViewSet):
    """
    Returns a summary of the weather data
    """

    permission_classes = (permissions.AllowAny,)

    def validate_query_params(self, params: Dict) -> None:
        """Validated the query params

        Args:
            params (dict): query params

        Raises:
            ValidationError: If the params are invalid
        """
        if not params.get("location"):
            raise ValidationError("The location query paramater is required.")

    def list(self, request):
        self.validate_query_params(request.query_params)

        try:
            lat, lon = latitude_longitude_from_location(
                request.query_params.get("location")
            )
        except AttributeError:
            raise ValidationError("Invalid location.")

        weather_client = OpenWeatherMapClient(lat, lon)

        period = request.query_params.get("period", None)

        if period:
            periods = period.split(",")
            if len(periods) > 1:
                period_start, period_end = periods
            else:
                period_start, period_end = periods[0], periods[0]

            period_start = int(period_start)
            period_end = int(period_end)

            weather_client.filter(period_start, period_end)

        return Response(
            dict(
                temp=dict(
                    avg=weather_client.average_temp(),
                    max=weather_client.max_temp(),
                    min=weather_client.min_temp(),
                    median=weather_client.median_temp(),
                ),
                humidity=dict(
                    avg=weather_client.average_humidity(),
                    max=weather_client.max_humidity(),
                    min=weather_client.min_humidity(),
                    median=weather_client.median_humidity(),
                ),
            ),
            status=200,
        )
