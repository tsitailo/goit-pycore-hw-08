from datetime import date

import pytest

from address_book.birthday import Birthday


class TestBirthday:
    def test_valid_date_initialization(self):
        birthday = Birthday("25.12.2000")
        assert isinstance(birthday.value, date)
        assert birthday.value == date(2000, 12, 25)

    def test_invalid_date_format(self):
        with pytest.raises(ValueError, match="Invalid date format. Use DD.MM.YYYY"):
            Birthday("2000-12-25")
        with pytest.raises(ValueError, match="Invalid date format. Use DD.MM.YYYY"):
            Birthday("25/12/2000")

    def test_invalid_date_range(self):
        with pytest.raises(ValueError, match="Invalid date range"):
            Birthday("32.12.2000")  # Invalid day
        with pytest.raises(ValueError, match="Invalid date range"):
            Birthday("25.13.2000")  # Invalid month
        with pytest.raises(ValueError, match="Invalid date range"):
            Birthday("25.12.1899")  # Year too early
        with pytest.raises(ValueError, match="Invalid date range"):
            Birthday("25.12.2101")  # Year too late

    def test_invalid_input_type(self):
        with pytest.raises(ValueError, match="Date must be a string"):
            Birthday(12252000)
        with pytest.raises(ValueError, match="Date must be a string"):
            Birthday(None)
        with pytest.raises(ValueError, match="Invalid date format. Use DD.MM.YYYY"):
            Birthday("abc.def.ghij")
