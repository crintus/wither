import os
import requests
import statistics
from typing import Dict
from datetime import datetime


class OpenWeatherMapClientError(Exception):
    pass


class OpenWeatherMapClient:
    """
    API client for the Open weather map API
    Supports:
        Daily forecast for 7 days
    """

    api_key = os.environ.get("OPEN_WEATHER_API_KEY")
    base_url = os.environ.get("OPEN_WEATHER_BASE_URL")

    @property
    def daily_data(self):
        return self.data.get("daily", [])

    def __init__(
        self, lat: str, lon: str,
    ):
        self.lat = lat
        self.lon = lon
        self.data = self.__get()

    def filter(self, period_start: int = None, period_end: int = None) -> None:
        """
        Filters the data based on the start and end periods

        Args:
            period_start (int, optional): [Timestamp of the period start]. Defaults to None.
            period_end (int, optional): [Timestamp of the period end]. Defaults to None.
        """
        if period_start:
            dt_start = datetime.fromtimestamp(period_start).replace(minute=0, second=0)
            self.data["daily"] = list(
                filter(
                    lambda daily: datetime.fromtimestamp(daily.get("dt")) >= dt_start,
                    self.daily_data,
                )
            )
        if period_end:
            dt_end = datetime.fromtimestamp(period_end).replace(minute=0, second=0)
            self.data["daily"] = list(
                filter(
                    lambda daily: datetime.fromtimestamp(daily.get("dt")) <= dt_end,
                    self.daily_data,
                )
            )

    def average_temp(self) -> float:
        return round(
            sum(
                [
                    sum(day["temp"].values()) / len(day["temp"])
                    for day in self.daily_data
                ]
            )
            / len(self.daily_data),
            2,
        )

    def max_temp(self) -> float:
        return round(max([day["temp"]["max"] for day in self.daily_data]), 2)

    def min_temp(self) -> float:
        return round(min([day["temp"]["min"] for day in self.daily_data]), 2)

    def median_temp(self) -> float:
        from itertools import chain

        merged_list = chain.from_iterable(
            [list(day["temp"].values()) for day in self.daily_data]
        )
        return round(statistics.median(sorted(merged_list)), 2)

    def average_humidity(self) -> float:
        return round(
            sum([day["humidity"] for day in self.daily_data]) / len(self.daily_data), 2,
        )

    def max_humidity(self) -> float:
        return round(max([day["humidity"] for day in self.daily_data]), 2)

    def min_humidity(self) -> float:
        return round(min([day["humidity"] for day in self.daily_data]), 2)

    def median_humidity(self) -> float:
        return round(
            statistics.median(sorted([day["humidity"] for day in self.daily_data])), 2
        )

    def get(self) -> None:
        self.data = self.__get()
        return self.data

    def __get(self, period_start: int = None) -> Dict:
        query_params = dict(
            appid=self.api_key,
            lat=self.lat,
            lon=self.lon,
            dt=period_start,
            exclude="current,minutely,hourly",
            units="metric",
        )
        response = requests.get(self.base_url, params=query_params)
        return response.json()
