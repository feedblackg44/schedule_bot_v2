from enums import LessonType


class Discipline:
    def __init__(self, name, emoji, lecture, command,
                 practice=None,
                 extra=None):
        self.name = name
        self.emoji = emoji
        self.command = command

        if not practice:
            practice = lecture

        self.teachers = {
            LessonType.LECTURE: lecture,
            LessonType.PRACTICE: practice
        }

        self.extra = extra

    def to_short_str(self, lesson_type, start_symbol=""):
        str_out = f"{start_symbol}{self.name}. <i>{lesson_type.value}</i> "

        teachers = [teacher.to_short_str() for teacher in self.teachers[lesson_type]]
        str_out += f"({', '.join(teachers)})"

        return str_out

    def __str__(self):
        str_out = f"{self.emoji} <b>{self.name}</b> {self.emoji}\n"
        str_out += f"Лекції:\n{self.to_short_str(LessonType.LECTURE, '- ')}\n"
        str_out += f"Практики:\n{self.to_short_str(LessonType.PRACTICE, '- ')}\n"
        if self.extra:
            str_out += f"Інше:\n"
            for extra in self.extra:
                str_out += f"- <a href='{extra['link']}'>{extra['name']}</a>\n"

        return str_out

