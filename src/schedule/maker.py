import logging

import yaml
from pydantic import ValidationError

from enums import Weekday

from .calendar import Day, DisciplineEntry, Lesson, TimeRange, Week
from .maker_models import ScheduleFileYaml
from .schedule import Schedule
from .university import Discipline, ExtraResource, Teacher

DAYS_KEYS: dict[str, Weekday] = {
    "monday": Weekday.MONDAY,
    "tuesday": Weekday.TUESDAY,
    "wednesday": Weekday.WEDNESDAY,
    "thursday": Weekday.THURSDAY,
    "friday": Weekday.FRIDAY,
    "saturday": Weekday.SATURDAY,
    "sunday": Weekday.SUNDAY,
}
DAYS_EMOJI = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]


class Maker:
    def __init__(self, path: str) -> None:
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.path: str = path

    def make(self) -> tuple[Schedule, dict[str, Teacher], dict[str, Discipline]]:
        self.logger.info(f"Загрузка расписания из файла {self.path}")
        with open(self.path, "r", encoding="UTF-8") as file:
            raw = yaml.safe_load(file)

        if raw is None:
            self.logger.error(f"Файл {self.path} пуст")
            return Schedule([], "", [], "", []), {}, {}

        try:
            schedule_file = ScheduleFileYaml.model_validate(raw)
        except ValidationError as e:
            self.logger.error(f"Файл {self.path} не прошёл валидацию:\n{e}")
            raise

        timetable: list[TimeRange] = [
            {"start": t.start, "end": t.end} for t in schedule_file.timetable
        ]

        teachers: dict[str, Teacher] = {
            t.name: Teacher(**t.model_dump()) for t in schedule_file.teachers
        }

        disciplines: dict[str, Discipline] = {}
        for d in schedule_file.disciplines:
            disciplines[d.name] = Discipline(
                name=d.name,
                command=d.command,
                lecture=[teachers[name] for name in d.lecture],
                practice=[teachers[name] for name in d.practice],
                extra=[ExtraResource(name=e.name, link=e.link) for e in d.extra],
                emoji=d.emoji,
            )

        weeks: list[Week] = []
        for w_idx, week in enumerate(schedule_file.schedule.values(), start=1):
            week_dict: dict[Weekday, Day] = {}
            for idx, (day, day_schedule) in enumerate(week.items()):
                day_dict: dict[int, Lesson] = {}
                for lesson_num, disc_list in day_schedule.items():
                    di_list: list[DisciplineEntry] = [
                        {
                            "discipline": disciplines[entry.name],
                            "is_lecture": entry.is_lecture,
                        }
                        for entry in disc_list
                    ]
                    day_dict[lesson_num] = Lesson(di_list, timetable[lesson_num - 1])
                week_dict[DAYS_KEYS[day]] = Day(DAYS_KEYS[day], DAYS_EMOJI[idx], day_dict)
            weeks.append(Week(w_idx, week_dict))

        return (
            Schedule(
                weeks,
                schedule_file.schedule_link,
                timetable,
                schedule_file.group,
                [ExtraResource(name=e.name, link=e.link) for e in schedule_file.extra],
            ),
            teachers,
            disciplines,
        )
