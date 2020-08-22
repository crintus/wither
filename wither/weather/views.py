from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from wither.open_weather_map.client import OpenWeatherMapClient
from wither.weather.serializers import WeatherSerializer


class WeatherViewSet(ViewSet):
    """
    Returns the raw weather data
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = WeatherSerializer

    def list(self, request):
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")

        try:
            date_start = int(request.query_params.get("date_start"))
        except TypeError:
            date_start = None

        try:
            date_end = int(request.query_params.get("date_end"))
        except TypeError:
            date_end = None

        weather_client = OpenWeatherMapClient(lat, lon)
        weather_client.filter(date_start, date_end)
        return Response(
            dict(
                temp=dict(
                    avg=weather_client.average(),
                    max=weather_client.max(),
                    min=weather_client.min(),
                ),
                humidity=dict(),
            ),
            status=200,
        )
