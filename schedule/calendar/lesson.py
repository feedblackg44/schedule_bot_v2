from enums import LessonType


class Lesson:
    def __init__(self, disciplines, start_and_end):
        self.disciplines = disciplines
        self.start_and_end = start_and_end

    def to_str_with_time(self):
        str_out = f"{self.start_and_end['start'].strftime('%H:%M')} - "
        str_out += str(self)
        return str_out

    def __str__(self):
        str_out = ""
        for idx, element in enumerate(self.disciplines):
            discipline = element['discipline']
            l_type = LessonType.LECTURE if element['is_lecture'] else LessonType.PRACTICE

            str_out += f"{'  ' if idx > 0 else ''}{discipline.to_short_str(l_type)}"
            if idx != len(self.disciplines) - 1:
                str_out += "\n"
        return str_out