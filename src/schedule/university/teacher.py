from typing import override


class Teacher:
    def __init__(self, name: str,
                 phone: str | None = None,
                 telegram: str | None = None,
                 email: str | None = None,
                 link: str | None = None):
        names = name.split()
        self.surname: str = names[0]
        self.name: str | None = names[1] if len(names) >= 2 else None
        self.patronymic: str | None = names[2] if len(names) >= 3 else None
        self.phone: str | None = phone
        self.telegram: str | None = telegram
        self.email: str | None = email
        self.link: str | None = link

    def to_short_str(self) -> str:
        return f"<a href='{self.link}'>{self.surname}</a>"

    @override
    def __str__(self) -> str:
        string_out = f"{self.surname} {self.name} {self.patronymic}"
        if self.telegram:
            string_out += f" (@{self.telegram})"
        elif self.email:
            string_out += f" ({self.email})"
        elif self.phone:
            string_out += f" ({self.phone})"
        else:
            string_out += " (немає контактів)"

        return string_out
