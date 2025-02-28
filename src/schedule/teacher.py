import logging


class Teacher:
    def __init__(self, name,
                 phone=None,
                 telegram=None,
                 email=None,
                 link=None):
        names = name.split()
        self.surname = names[0]
        self.name = names[1] if len(names) >= 2 else None
        self.patronymic = names[2] if len(names) >= 3 else None
        self.phone = phone
        self.telegram = telegram
        self.email = email
        self.link = link

    def to_short_str(self):
        return f"<a href='{self.link}'>{self.surname}</a>"

    def __str__(self):
        string_out = f"{self.surname} {self.name} {self.patronymic}"
        if self.telegram:
            string_out += f" (@{self.telegram})"
        elif self.email:
            string_out += f" ({self.email})"
        elif self.phone:
            string_out += f" ({self.phone})"
        else:
            string_out += f" (немає контактів)"

        return string_out