

class Day:
    def __init__(self, name, emoji, lessons):
        self.name = name.value if hasattr(name, "value") else name
        self.emoji = emoji
        self.lessons = lessons

    def to_str(self, use_time=False):
        str_out = f"{self.emoji} {str(self.name)} {self.emoji}\n"
        for i, (idx, lesson) in enumerate(self.lessons.items(), start=1):
            str_out += f"{idx}. {lesson.to_str_with_time() if use_time else str(lesson)}"
            if i != len(self.lessons):
                str_out += "\n"
        return str_out

    def __str__(self):
        return self.to_str()
