from datetime import datetime, timedelta

from config import FIRST_WEEK_NUMBER
from enums import Weekday, WeekType


def get_current_week_number(week: WeekType = WeekType.CURRENT) -> int:
    current_week_number = datetime.now().isocalendar()[1]  # noqa: DTZ005
    if week == WeekType.CURRENT:
        return (current_week_number + FIRST_WEEK_NUMBER) % 2
    elif week == WeekType.NEXT:
        return (current_week_number + FIRST_WEEK_NUMBER + 1) % 2
    elif week == WeekType.FIRST:
        return 0 if FIRST_WEEK_NUMBER == 0 else 1
    elif week == WeekType.SECOND:
        return 1 if FIRST_WEEK_NUMBER == 0 else 0
    else:
        raise ValueError("Invalid week type")


def get_current_day(next_day: bool = False) -> Weekday:
    todate = datetime.now()  # noqa: DTZ005
    if next_day:
        todate = todate + timedelta(days=1)
    match todate.weekday():
        case 0:
            return Weekday.MONDAY
        case 1:
            return Weekday.TUESDAY
        case 2:
            return Weekday.WEDNESDAY
        case 3:
            return Weekday.THURSDAY
        case 4:
            return Weekday.FRIDAY
        case 5:
            return Weekday.SATURDAY
        case 6:
            return Weekday.SUNDAY
        case _:
            raise ValueError(f"Unexpected weekday number: {todate.weekday()}")


def declination(plural_word_234: str, single_word: str, plural_word: str, amount: int) -> str:
    if 4 >= amount % 10 >= 2 and (amount % 100 < 12 or amount % 100 > 14):
        return plural_word_234
    elif amount % 10 == 1 and amount % 100 != 11:
        return single_word
    else:
        return plural_word


def get_str_datetime(diff: timedelta) -> str:
    total_seconds = int(diff.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    str_out = "<b>"
    if hours > 0:
        str_out += f"{hours} {declination('години', 'година', 'годин', hours)} "
    if minutes > 0:
        str_out += f"{minutes} {declination('хвилини', 'хвилина', 'хвилин', minutes)} "
    if seconds > 0:
        str_out += f"{seconds} {declination('секунди', 'секунда', 'секунд', seconds)} "
    str_out += "</b>"
    if str_out == "":
        str_out = "<b>0 секунд</b>"

    return str_out
