from datetime import time

from pydantic import BaseModel, field_validator


class TimetableEntryYaml(BaseModel):
    start: time
    end: time

    @field_validator("start", "end", mode="before")
    @classmethod
    def parse_time(cls, value: str) -> time:
        return time.fromisoformat(value)


class TeacherYaml(BaseModel):
    name: str
    telegram: str | None = None
    phone: str | None = None
    email: str | None = None
    link: str | None = None


class ExtraResourceYaml(BaseModel):
    name: str
    link: str


class DisciplineYaml(BaseModel):
    name: str
    command: str
    lecture: list[str]
    practice: list[str] = []
    extra: list[ExtraResourceYaml] = []
    emoji: str

    @field_validator("lecture", "practice", mode="before")
    @classmethod
    def normalize_teacher_list(cls, value: str | list[str] | None) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        return value


class LessonEntryYaml(BaseModel):
    name: str
    is_lecture: bool


class ScheduleFileYaml(BaseModel):
    timetable: list[TimetableEntryYaml]
    teachers: list[TeacherYaml]
    disciplines: list[DisciplineYaml]
    schedule: dict[str, dict[str, dict[int, list[LessonEntryYaml]]]]
    schedule_link: str
    group: str
    extra: list[ExtraResourceYaml] = []
