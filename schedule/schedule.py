import logging
from datetime import datetime

from enums import WeekType
from utils import get_current_week_number, get_str_datetime


class Schedule:
    def __init__(self, weeks, link, timetable, group, extra=None):
        self.weeks = weeks
        self.link = link
        self.timetable = timetable
        self.group = group
        self.extra = extra

        self.week_keys = [WeekType.FIRST,
                          WeekType.SECOND]
        self.logger = logging.getLogger(__name__)

    def left(self):
        cur_time = datetime.now().time()
        today_day = self.today()
        if isinstance(today_day, str):
            return today_day

        today_timetable = []
        for lesson in today_day.lessons:
            today_timetable.append({"type": "start", "time": self.timetable[lesson - 1]["start"]})
            today_timetable.append({"type": "end", "time": self.timetable[lesson - 1]["end"]})

        next_time = None
        for i in range(len(today_timetable) - 1, -1, -1):
            if today_timetable[i]["time"] < cur_time:
                if i < len(today_timetable) - 1:
                    next_time = today_timetable[i + 1]
                break

        if not next_time:
            return "Сьогодні занять не залишилось 😊"

        cur_time = datetime.combine(datetime.now().date(), cur_time)
        next_time["time"] = datetime.combine(datetime.now().date(), next_time["time"])

        self.logger.info(f"cur_time: {cur_time}, next_time: {next_time['time']}")

        diff = next_time["time"] - cur_time
        diff = datetime.utcfromtimestamp(diff.total_seconds())
        self.logger.info(f"diff: {diff}")

        str_diff = get_str_datetime(diff)

        if next_time["type"] == "start":
            return f"⏱ До початку пари залишилось: {str_diff}"
        else:
            return f"⏱ До кінця пари залишилось: {str_diff}"

    def today(self):
        self.logger.debug(get_current_week_number(WeekType.CURRENT))
        if today_day := self.weeks[get_current_week_number(WeekType.CURRENT)].today():
            return today_day
        else:
            return "Сьогодні вихідний 😊"

    def tomorrow(self):
        if tomorrow_day := self.weeks[get_current_week_number(WeekType.CURRENT)].tomorrow():
            return tomorrow_day
        else:
            return "Завтра вихідний 😊"

    def str_extra(self):
        str_out = ""
        if self.extra:
            str_out += "🔔 Додаткова інформація 🔔\n\n"
            for extra in self.extra:
                str_out += f"- <a href='{extra['link']}'>{extra['name']}</a>\n"
        return str_out

    def to_str(self, week=WeekType.ALL):
        if week == WeekType.ALL:
            return str(self)
        else:
            week_number = get_current_week_number(week)
            str_out = f"📅 {week} тиждень 📅\n\n"
            str_out += f"{self.weeks[week_number]}"
            return str_out

    def __str__(self):
        str_out = ""
        for idx, week in enumerate(self.weeks):
            str_out += self.to_str(week=self.week_keys[idx])
            if idx != len(self.weeks):
                str_out += "\n\n"
        return str_out
