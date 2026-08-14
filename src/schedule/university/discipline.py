from typing import TypedDict, override

from enums import LessonType

from .teacher import Teacher


class ExtraResource(TypedDict):
    """Represents an extra resource for a discipline."""
    name: str
    link: str


class Discipline:
    def __init__(
        self,
        name: str,
        emoji: str,
        lecture: list[Teacher],
        command: str,
        practice: list[Teacher] | None = None,
        extra: list[ExtraResource] | None = None,
    ) -> None:
        self.name: str = name
        self.emoji: str = emoji
        self.command: str = command

        if not practice:
            practice = lecture

        self.teachers: dict[LessonType, list[Teacher]] = {
            LessonType.LECTURE: lecture,
            LessonType.PRACTICE: practice,
        }

        self.extra: list[ExtraResource] | None = extra

    def to_short_str(self, lesson_type: LessonType, start_symbol: str = "") -> str:
        str_out = f"{start_symbol}{self.name}. <i>{lesson_type.value}</i> "

        teachers = [teacher.to_short_str() for teacher in self.teachers[lesson_type]]
        str_out += f"({', '.join(teachers)})"

        return str_out

    @override
    def __str__(self) -> str:
        str_out = f"{self.emoji} <b>{self.name}</b> {self.emoji}\n"
        str_out += f"Лекції:\n{self.to_short_str(LessonType.LECTURE, '- ')}\n"
        str_out += f"Практики:\n{self.to_short_str(LessonType.PRACTICE, '- ')}\n"
        if self.extra:
            str_out += "Інше:\n"
            for extra in self.extra:
                str_out += f"- <a href='{extra['link']}'>{extra['name']}</a>\n"

        return str_out
