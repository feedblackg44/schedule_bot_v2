import logging
from typing import override

from enums import Weekday
from utils import get_current_day

from .day import Day


class Week:
    def __init__(self, number: int, days: dict[Weekday, Day]) -> None:
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.number: int = number
        self.days: dict[Weekday, Day] = days

    def today(self) -> Day | None:
        return self.days.get(get_current_day())

    def tomorrow(self) -> Day | None:
        return self.days.get(get_current_day(next_day=True))

    @override
    def __str__(self) -> str:
        str_out = ""
        for idx, day in enumerate(self.days.values(), start=1):
            str_out += f"{day}"
            if idx != len(self.days):
                str_out += "\n\n"
        return str_out
