from typing import Tuple


def latitude_longitude_from_location(location: str) -> Tuple[int, int]:
    """Returns the latitude and longitude for a location string

    Args:
        location (str): Location string eg. "Cape Town"

    Returns:
        list[int, int]: With latitude and longitude

    Raises:
        AttributeError: When location is not valid
    """
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="wither")
    location = geolocator.geocode(location)
    return location.latitude, location.longitude
