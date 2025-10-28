from datetime import datetime
from .field import Field


class Birthday(Field):

    def __init__(self, value):
        super().__init__(value)
        if not isinstance(value, str):
            raise ValueError("Date must be a string")

        try:
            day, month, year = map(int, value.split('.'))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100):
            raise ValueError("Invalid date range")

        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
