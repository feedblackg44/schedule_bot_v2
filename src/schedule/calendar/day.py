from typing import override

from enums import Weekday

from .lesson import Lesson


class Day:
    def __init__(self, name: Weekday, emoji: str, lessons: dict[int, Lesson]):
        self.name: str = name.value
        self.emoji: str = emoji
        self.lessons: dict[int, Lesson] = lessons

    def to_str(self, use_time: bool = False) -> str:
        str_out = f"{self.emoji} {self.name!s} {self.emoji}\n"
        for i, (idx, lesson) in enumerate(self.lessons.items(), start=1):
            str_out += f"{idx}. {lesson.to_str_with_time() if use_time else str(lesson)}"
            if i != len(self.lessons):
                str_out += "\n"
        return str_out

    @override
    def __str__(self) -> str:
        return self.to_str()
