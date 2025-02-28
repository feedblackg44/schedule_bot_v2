import logging

from utils import get_current_day


class Week:
    def __init__(self, number, days):
        self.logger = logging.getLogger(__name__)

        self.number = number
        self.days = days

    def today(self):
        return self.days.get(get_current_day())

    def tomorrow(self):
        return self.days.get(get_current_day(next_day=True))

    def __str__(self):
        str_out = ""
        for idx, day in enumerate(self.days.values(), start=1):
            str_out += f"{day}"
            if idx != len(self.days):
                str_out += "\n\n"
        return str_out
