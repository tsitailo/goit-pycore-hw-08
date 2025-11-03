"""Тести для класу AddressBook."""

import sys
import unittest
from datetime import timedelta, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from address_book import AddressBook, Record


class TestAddressBook(unittest.TestCase):
    """Тести для класу AddressBook"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.book = AddressBook()

    def test_address_book_creation(self):
        """Тест створення адресної книги"""
        self.assertEqual(len(self.book.data), 0)

    def test_change_existing_contact(self):
        """Тест зміни телефону для існуючого контакту"""
        record = Record("John")
        record.add_phone("1234567890")
        self.book.add_record(record)
        self.assertTrue(self.book.change("John", "1234567890", "9876543210"))

    def test_change_nonexistent_contact(self):
        """Тест зміни телефону для неіснуючого контакту"""
        self.assertFalse(self.book.change("NonExistent", "1234567890", "9876543210"))

    def test_change_invalid_phone(self):
        """Тест зміни на некоректний телефон"""
        record = Record("John")
        record.add_phone("1234567890")
        self.book.add_record(record)
        with self.assertRaises(ValueError):
            self.book.change("John", "1234567890", "invalid")

    def test_add_record(self):
        """Тест додавання запису"""
        record = Record("John")
        self.book.add_record(record)
        self.assertEqual(len(self.book.data), 1)
        self.assertIn("John", self.book.data)

    def test_add_multiple_records(self):
        """Тест додавання декількох записів"""
        john = Record("John")
        jane = Record("Jane")
        self.book.add_record(john)
        self.book.add_record(jane)
        self.assertEqual(len(self.book.data), 2)

    def test_add_duplicate_name(self):
        """Тест додавання запису з дублікатом імені (перезапис)"""
        john1 = Record("John")
        john1.add_phone("1234567890")
        self.book.add_record(john1)

        john2 = Record("John")
        john2.add_phone("9876543210")
        self.book.add_record(john2)

        self.assertEqual(len(self.book.data), 1)
        # Перевіряємо, що запис був перезаписаний
        found = self.book.find("John")
        self.assertEqual(len(found.phones), 1)
        self.assertEqual(found.phones[0].value, "9876543210")

    def test_add_invalid_record(self):
        """Тест додавання невалідного запису"""
        with self.assertRaises(TypeError):
            self.book.add_record("Not a record")

    def test_find_existing_record(self):
        """Тест пошуку існуючого запису"""
        record = Record("John")
        self.book.add_record(record)
        found = self.book.find("John")
        self.assertIsNotNone(found)
        self.assertEqual(found.name.value, "John")

    def test_find_nonexistent_record(self):
        """Тест пошуку неіснуючого запису"""
        found = self.book.find("NonExistent")
        self.assertIsNone(found)

    def test_find_case_sensitive(self):
        """Тест що пошук чутливий до регістру"""
        record = Record("John")
        self.book.add_record(record)
        found = self.book.find("john")
        self.assertIsNone(found)

    def test_delete_existing_record(self):
        """Тест видалення існуючого запису"""
        record = Record("John")
        self.book.add_record(record)
        self.book.delete("John")
        self.assertEqual(len(self.book.data), 0)

    def test_delete_nonexistent_record(self):
        """Тест видалення неіснуючого запису"""
        with self.assertRaises(KeyError) as context:
            self.book.delete("NonExistent")
        self.assertIn("not found", str(context.exception))

    def test_delete_from_empty_book(self):
        """Тест видалення з порожньої книги"""
        with self.assertRaises(KeyError):
            self.book.delete("John")

    def test_userdict_functionality(self):
        """Тест функціональності UserDict"""
        record = Record("John")
        self.book.add_record(record)
        # Перевіряємо доступ через індексацію
        self.assertEqual(self.book.data["John"].name.value, "John")
        # Перевіряємо ітерацію
        for name, rec in self.book.data.items():
            self.assertIsInstance(rec, Record)

    def test_str_empty_book(self):
        """Тест строкового представлення порожньої книги"""
        result = str(self.book)
        self.assertIn("empty", result.lower())

    def test_str_with_records(self):
        """Тест строкового представлення з записами"""
        john = Record("John")
        john.add_phone("1234567890")
        self.book.add_record(john)

        result = str(self.book)
        self.assertIn("John", result)
        self.assertIn("1234567890", result)

    def test_repr(self):
        """Тест представлення адресної книги"""
        john = Record("John")
        self.book.add_record(john)

        result = repr(self.book)
        self.assertIn("AddressBook", result)
        self.assertIn("1", result)

    def test_address_book_integration(self):
        """Тест комплексного використання адресної книги"""
        # Створення запису для John
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")
        self.book.add_record(john_record)

        # Створення та додавання нового запису для Jane
        jane_record = Record("Jane")
        jane_record.add_phone("9876543210")
        self.book.add_record(jane_record)

        # Перевірка кількості записів
        self.assertEqual(len(self.book.data), 2)

        # Знаходження та редагування телефону для John
        john = self.book.find("John")
        john.edit_phone("1234567890", "1112223333")

        # Перевірка зміни телефону
        self.assertEqual(john.phones[0].value, "1112223333")

        # Пошук конкретного телефону у записі John
        found_phone = john.find_phone("5555555555")
        self.assertEqual(found_phone.value, "5555555555")

        # Видалення запису Jane
        self.book.delete("Jane")
        self.assertEqual(len(self.book.data), 1)

    def test_get_upcoming_birthdays_empty_book(self):
        """Тест отримання днів народження з порожньої книги"""
        result = self.book.get_upcoming_birthdays()
        self.assertEqual(result, [])

    def test_get_upcoming_birthdays_no_birthdays(self):
        """Тест з контактами без днів народження"""
        john = Record("John")
        john.add_phone("1234567890")
        self.book.add_record(john)

        jane = Record("Jane")
        jane.add_phone("9876543210")
        self.book.add_record(jane)

        result = self.book.get_upcoming_birthdays()
        self.assertEqual(result, [])

    def test_get_upcoming_birthdays_within_week(self):
        """Тест з днем народження протягом тижня"""
        today = datetime.today().date()
        upcoming_date = today + timedelta(days=3)

        john = Record("John")
        john.add_birthday(upcoming_date.strftime("%d.%m.1990"))
        self.book.add_record(john)

        result = self.book.get_upcoming_birthdays()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "John")

    def test_get_upcoming_birthdays_today(self):
        """Тест з днем народження сьогодні"""
        today = datetime.today().date()

        john = Record("John")
        john.add_birthday(today.strftime("%d.%m.1990"))
        self.book.add_record(john)

        result = self.book.get_upcoming_birthdays()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "John")

    def test_get_upcoming_birthdays_outside_week(self):
        """Тест з днем народження за межами тижня"""
        today = datetime.today().date()
        far_date = today + timedelta(days=10)

        john = Record("John")
        john.add_birthday(far_date.strftime("%d.%m.1990"))
        self.book.add_record(john)

        result = self.book.get_upcoming_birthdays()
        self.assertEqual(len(result), 0)

    def test_get_upcoming_birthdays_past_this_year(self):
        """Тест з днем народження що вже минув цього року"""
        today = datetime.today().date()
        past_date = today - timedelta(days=10)

        john = Record("John")
        john.add_birthday(past_date.strftime("%d.%m.1990"))
        self.book.add_record(john)

        result = self.book.get_upcoming_birthdays()
        self.assertEqual(len(result), 0)

    def test_get_upcoming_birthdays_on_saturday(self):
        """Тест переносу вітання з суботи на понеділок"""
        today = datetime.today().date()

        # Знаходимо наступну суботу
        days_ahead = 5 - today.weekday()  # 5 = субота
        if days_ahead <= 0:
            days_ahead += 7
        next_saturday = today + timedelta(days=days_ahead)

        john = Record("John")
        john.add_birthday(next_saturday.strftime("%d.%m.1990"))
        self.book.add_record(john)

        result = self.book.get_upcoming_birthdays()
        if len(result) > 0:  # Якщо субота потрапляє в діапазон 7 днів
            congratulation_date = datetime.strptime(result[0]["congratulation_date"], "%d.%m.%Y").date()
            # Перевіряємо що це понеділок
            self.assertEqual(congratulation_date.weekday(), 0)

    def test_get_upcoming_birthdays_on_sunday(self):
        """Тест переносу вітання з неділі на понеділок"""
        today = datetime.today().date()

        # Знаходимо наступну неділю
        days_ahead = 6 - today.weekday()  # 6 = неділя
        if days_ahead <= 0:
            days_ahead += 7
        next_sunday = today + timedelta(days=days_ahead)

        john = Record("John")
        john.add_birthday(next_sunday.strftime("%d.%m.1990"))
        self.book.add_record(john)

        result = self.book.get_upcoming_birthdays()
        if len(result) > 0:  # Якщо неділя потрапляє в діапазон 7 днів
            congratulation_date = datetime.strptime(result[0]["congratulation_date"], "%d.%m.%Y").date()
            # Перевіряємо що це понеділок
            self.assertEqual(congratulation_date.weekday(), 0)

    def test_get_upcoming_birthdays_multiple_contacts(self):
        """Тест з декількома контактами з днями народження"""
        today = datetime.today().date()
        date1 = today + timedelta(days=2)
        date2 = today + timedelta(days=5)

        john = Record("John")
        john.add_birthday(date1.strftime("%d.%m.1990"))
        self.book.add_record(john)

        jane = Record("Jane")
        jane.add_birthday(date2.strftime("%d.%m.1985"))
        self.book.add_record(jane)

        result = self.book.get_upcoming_birthdays()
        self.assertEqual(len(result), 2)
        names = [item["name"] for item in result]
        self.assertIn("John", names)
        self.assertIn("Jane", names)

    def test_get_upcoming_birthdays_custom_days(self):
        """Тест з користувацьким діапазоном днів"""
        today = datetime.today().date()
        date_in_14_days = today + timedelta(days=14)

        john = Record("John")
        john.add_birthday(date_in_14_days.strftime("%d.%m.1990"))
        self.book.add_record(john)

        # З діапазоном 7 днів не повинно бути результатів
        result_7 = self.book.get_upcoming_birthdays(days=7)
        self.assertEqual(len(result_7), 0)

        # З діапазоном 20 днів повинен бути результат
        result_20 = self.book.get_upcoming_birthdays(days=20)
        self.assertEqual(len(result_20), 1)

    def test_get_upcoming_birthdays_leap_year(self):
        """Тест з днем народження 29 лютого"""
        today = datetime.today().date()

        # Якщо зараз близько до 29 лютого, тестуємо
        john = Record("John")
        john.add_birthday("29.02.1992")  # Високосний рік
        self.book.add_record(john)

        # Функція не повинна падати з помилкою
        result = self.book.get_upcoming_birthdays()
        self.assertIsInstance(result, list)

    def test_get_upcoming_birthdays_result_format(self):
        """Тест формату результату"""
        today = datetime.today().date()
        upcoming_date = today + timedelta(days=3)

        john = Record("John")
        john.add_birthday(upcoming_date.strftime("%d.%m.1990"))
        self.book.add_record(john)

        result = self.book.get_upcoming_birthdays()
        self.assertEqual(len(result), 1)

        # Перевіряємо структуру словника
        self.assertIn("name", result[0])
        self.assertIn("congratulation_date", result[0])

        # Перевіряємо формат дати
        date_str = result[0]["congratulation_date"]
        self.assertRegex(date_str, r'\d{2}\.\d{2}\.\d{4}')


if __name__ == "__main__":
    unittest.main(verbosity=2)
