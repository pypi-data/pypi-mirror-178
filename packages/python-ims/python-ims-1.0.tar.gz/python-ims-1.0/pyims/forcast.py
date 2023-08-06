from datetime import datetime
from typing import Dict

class Forcast:
    days: list

    def __init__(self,days: list = []):
        self.days = days


class Daily:
    date: datetime
    location: str
    day: str
    weather: str
    minimum_temperature: int
    maximum_temperature: int
    maximum_uvi: int
    hours: list
    description: str

    def __init__(self, date: datetime, location: str, day: str,weather: str, minimum_temperature: int, maximum_temperature: int, maximum_uvi: int, description: str, hours: list = []) -> None:
        self.date = date
        self.location = location
        self.day = day
        self.weather = weather
        self.minimum_temperature = minimum_temperature
        self.maximum_temperature = maximum_temperature
        self.maximum_uvi = maximum_uvi
        description = description
        self.hours = hours


class Hourly:
    hour: str
    weather: str
    temperature: int

    def __init__(self,hour: str, weather: str, temperature: int) -> None:
        self.hour = hour
        self.weather = weather
        self.temperature = temperature