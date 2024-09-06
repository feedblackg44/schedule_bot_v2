from datetime import datetime, timedelta

from enums import WeekType, Weekday
from config import FIRST_WEEK_NUMBER


def get_current_week_number(week=WeekType.CURRENT):
    current_week_number = datetime.now().isocalendar()[1]
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

def get_current_day(next_day=False):
    todate = datetime.now()
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

def declination(plural_word_234, single_word, plural_word, amount):
    if 4 >= amount % 10 >= 2 and (amount % 100 < 12 or amount % 100 > 14):
        return plural_word_234
    elif amount % 10 == 1 and amount % 100 != 11:
        return single_word
    else:
        return plural_word

def get_str_datetime(time: datetime):
    if time is None:
        return ""

    str_out = "<b>"
    if time.hour > 0:
        str_out += f"{time.hour} {declination('години', 'година', 'годин', time.hour)} "
    if time.minute > 0:
        str_out += f"{time.minute} {declination('хвилини', 'хвилина', 'хвилин', time.minute)} "
    if time.second > 0:
        str_out += f"{time.second} {declination('секунди', 'секунда', 'секунд', time.second)} "
    str_out += "</b>"
    if str_out == "":
        str_out = "<b>0 секунд</b>"

    return str_out