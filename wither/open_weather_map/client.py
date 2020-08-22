import os
import requests
import functools
from datetime import datetime


class OpenWeatherMapClient:
    """
    API client for the Open weather map API
    Supports:
        Daily forecast for 7 days
        Historical data for the previous 5 days
    """

    api_key = os.environ.get("OPEN_WEATHER_API_KEY")
    base_url = os.environ.get("OPEN_WEATHER_BASE_URL")

    def __init__(
        self, lat: str, lon: str,
    ):
        self.lat = lat
        self.lon = lon
        self.data = None
        self.filtered_data = None

    def filter(self, date_start: int = None, date_end: int = None):
        # Store as datetime object for better manipulation
        # Set hours and minutes to only work with the day timestamps of the consumed api
        date_start = (
            datetime.fromtimestamp(date_start).replace(hour=12, minute=0, second=0)
            if date_start
            else None
        )
        date_end = (
            datetime.fromtimestamp(date_end).replace(hour=12, minute=0, second=0)
            if date_end
            else None
        )

        date_start_timestamp = int(date_start.timestamp())
        self.data = self.__get(date_start_timestamp).get("daily")
        self.filtered_data = self.data
        # Filter our date based on the selected dates
        if date_start:
            self.filtered_data = list(
                filter(
                    lambda daily: datetime.fromtimestamp(daily.get("dt")) > date_start,
                    self.filtered_data,
                )
            )
        if date_end:
            self.filtered_data = list(
                filter(
                    lambda daily: datetime.fromtimestamp(daily.get("dt")) < date_end,
                    self.filtered_data,
                )
            )

    def average(self):
        return round(
            sum(
                [
                    (day["temp"]["min"] + day["temp"]["max"]) / 2
                    for day in self.filtered_data
                ]
            )
            / len(self.filtered_data),
            2,
        )

    def max(self):
        return max([day["temp"]["max"] for day in self.filtered_data])

    def min(self):
        return min([day["temp"]["min"] for day in self.filtered_data])

    def get(self):
        return self.__get()

    def __date_start_filter(self, daily, date_start):
        date_object = datetime.fromtimestamp(daily.get("dt"))
        return date_object > date_start

    def __date_end_filter(self, daily, date_end):
        date_object = datetime.fromtimestamp(daily.get("dt"))
        return date_object < date_end

    def __get(self, date_start):
        query_params = dict(
            appid=self.api_key,
            lat=self.lat,
            lon=self.lon,
            dt=date_start,
            exclude="current,minutely,hourly",
            units="metric",
        )
        response = requests.get(self.base_url, params=query_params)
        return response.json()
