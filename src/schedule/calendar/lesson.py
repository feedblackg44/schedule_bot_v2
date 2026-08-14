from datetime import time
from typing import TypedDict, override

from enums import LessonType
from schedule.university import Discipline


class DisciplineEntry(TypedDict):
    """Represents a discipline entry in a lesson."""
    discipline: Discipline
    is_lecture: bool


class TimeRange(TypedDict):
    """Represents a time range for a lesson."""
    start: time
    end: time


class Lesson:
    def __init__(self, disciplines: list[DisciplineEntry], start_and_end: TimeRange) -> None:
        self.disciplines: list[DisciplineEntry] = disciplines
        self.start_and_end: TimeRange = start_and_end

    def to_str_with_time(self) -> str:
        str_out = f"{self.start_and_end['start'].strftime('%H:%M')} - "
        str_out += str(self)
        return str_out

    @override
    def __str__(self) -> str:
        str_out = ""
        for idx, element in enumerate(self.disciplines):
            discipline = element["discipline"]
            l_type = LessonType.LECTURE if element["is_lecture"] else LessonType.PRACTICE

            str_out += f"{'  ' if idx > 0 else ''}{discipline.to_short_str(l_type)}"
            if idx != len(self.disciplines) - 1:
                str_out += "\n"
        return str_out
