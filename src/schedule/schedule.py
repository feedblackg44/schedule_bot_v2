import logging
from datetime import datetime, time
from typing import Literal, override

from enums import WeekType
from utils import get_current_week_number, get_str_datetime

from .calendar import Day, TimeRange, Week
from .university import ExtraResource


class Schedule:
    def __init__(
        self,
        weeks: list[Week],
        link: str,
        timetable: list[TimeRange],
        group: str,
        extra: list[ExtraResource] | None = None,
    ) -> None:
        self.weeks: list[Week] = weeks
        self.link: str = link
        self.timetable: list[TimeRange] = timetable
        self.group: str = group
        self.extra: list[ExtraResource] | None = extra

        self.week_keys: list[WeekType] = [WeekType.FIRST, WeekType.SECOND]
        self.logger: logging.Logger = logging.getLogger(__name__)

    def left(self) -> str:
        cur_time = datetime.now().time()  # noqa: DTZ005
        today_day = self.today()
        if isinstance(today_day, str):
            return today_day

        events: list[tuple[Literal["start", "end"], time]] = []
        for lesson_num in today_day.lessons:
            events.append(("start", self.timetable[lesson_num - 1]["start"]))
            events.append(("end", self.timetable[lesson_num - 1]["end"]))

        next_event: tuple[Literal["start", "end"], time] | None = None
        for i in range(len(events) - 1, -1, -1):
            if events[i][1] < cur_time:
                if i < len(events) - 1:
                    next_event = events[i + 1]
                break

        if not next_event:
            return "Сьогодні занять не залишилось 😊"

        next_type, next_time_value = next_event
        cur_dt = datetime.combine(datetime.now().date(), cur_time)  # noqa: DTZ005
        next_dt = datetime.combine(datetime.now().date(), next_time_value)  # noqa: DTZ005

        self.logger.info(f"cur_time: {cur_dt}, next_time: {next_dt}")

        diff = next_dt - cur_dt
        self.logger.info(f"diff: {diff}")

        str_diff = get_str_datetime(diff)

        if next_type == "start":
            return f"⏱ До початку пари залишилось: {str_diff}"
        else:
            return f"⏱ До кінця пари залишилось: {str_diff}"

    def today(self) -> Day | str:
        self.logger.debug(get_current_week_number(WeekType.CURRENT))
        if today_day := self.weeks[get_current_week_number(WeekType.CURRENT)].today():
            return today_day
        else:
            return "Сьогодні вихідний 😊"

    def tomorrow(self) -> Day | str:
        if tomorrow_day := self.weeks[get_current_week_number(WeekType.CURRENT)].tomorrow():
            return tomorrow_day
        else:
            return "Завтра вихідний 😊"

    def str_extra(self) -> str:
        str_out = ""
        if self.extra:
            str_out += "🔔 Додаткова інформація 🔔\n\n"
            for extra in self.extra:
                str_out += f"- <a href='{extra['link']}'>{extra['name']}</a>\n"
        return str_out

    def to_str(self, week: WeekType = WeekType.ALL) -> str:
        if week == WeekType.ALL:
            return str(self)
        else:
            week_number = get_current_week_number(week)
            str_out = f"📅 {week} тиждень 📅\n\n"
            str_out += f"{self.weeks[week_number]}"
            return str_out

    @override
    def __str__(self) -> str:
        str_out = ""
        for idx, _ in enumerate(self.weeks):
            str_out += self.to_str(week=self.week_keys[idx])
            if idx != len(self.weeks):
                str_out += "\n\n"
        return str_out
