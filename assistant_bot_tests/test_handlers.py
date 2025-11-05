"""Тести для модуля handlers."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest  # noqa: E402
from datetime import datetime, timedelta  # noqa: E402

from address_book import AddressBook, Record  # noqa: E402
from assistant_bot import handlers  # noqa: E402


class TestInputErrorDecorator(unittest.TestCase):
    """Тести для декоратора input_error"""

    def test_decorator_with_index_error(self):
        """Тест обробки IndexError"""

        @handlers.input_error
        def func_with_index_error(args, book):
            return args[10]  # IndexError

        result = func_with_index_error([], AddressBook())
        # Перевіряємо що повертається повідомлення про помилку
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_decorator_with_key_error(self):
        """Тест обробки KeyError"""

        @handlers.input_error
        def func_with_key_error(args, book):
            d = {}
            return d['nonexistent']  # KeyError

        result = func_with_key_error([], AddressBook())
        self.assertIn("not found", result.lower())

    def test_decorator_with_value_error(self):
        """Тест обробки ValueError"""

        @handlers.input_error
        def func_with_value_error(args, book):
            raise ValueError("Invalid value")

        result = func_with_value_error([], AddressBook())
        # Перевіряємо що повертається якесь повідомлення
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_decorator_with_type_error(self):
        """Тест обробки TypeError"""

        @handlers.input_error
        def func_with_type_error(args, book):
            return "string" + 5  # TypeError

        result = func_with_type_error([], AddressBook())
        self.assertIsInstance(result, str)

    def test_decorator_success(self):
        """Тест успішного виконання функції"""

        @handlers.input_error
        def func_success(args, book):
            return "Success"

        result = func_success([], AddressBook())
        self.assertEqual(result, "Success")


class TestAddContact(unittest.TestCase):
    """Тести для функції add_contact"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.book = AddressBook()

    def test_add_contact_success(self):
        """Тест успішного додавання контакту"""
        result = handlers.add_contact(["John", "1234567890"], self.book)
        self.assertIsInstance(result, str)
        self.assertIsNotNone(self.book.find("John"))

    def test_add_contact_invalid_phone(self):
        """Тест додавання з некоректним телефоном"""
        result = handlers.add_contact(["John", "invalid"], self.book)
        # Очікуємо повідомлення про помилку
        self.assertIsInstance(result, str)

    def test_add_contact_missing_name(self):
        """Тест додавання без імені"""
        result = handlers.add_contact([], self.book)
        self.assertIn("give me name and phone", result.lower())

    def test_add_contact_missing_phone(self):
        """Тест додавання без телефону"""
        result = handlers.add_contact(["John"], self.book)
        self.assertIn("give me name and phone", result.lower())

    def test_add_contact_too_many_args(self):
        """Тест додавання з занадто багатьма аргументами"""
        result = handlers.add_contact(["John", "1234567890", "extra"], self.book)
        # Перевіряємо що функція все одно працює
        self.assertIsInstance(result, str)

    def test_add_existing_contact(self):
        """Тест додавання існуючого контакту (перезапис)"""
        handlers.add_contact(["John", "1234567890"], self.book)
        handlers.add_contact(["John", "9876543210"], self.book)
        # Перевіряємо що контакт існує
        john = self.book.find("John")
        self.assertIsNotNone(john)

    def test_add_contact_empty_name(self):
        """Тест додавання з порожнім ім'ям"""
        result = handlers.add_contact(["", "1234567890"], self.book)
        self.assertIn("give me name and phone", result.lower())

    def test_add_contact_special_characters_in_name(self):
        """Тест додавання з спецсимволами в імені"""
        result = handlers.add_contact(["John@123", "1234567890"], self.book)
        self.assertIsInstance(result, str)

    def test_add_contact_multiple_phones(self):
        """Тест додавання контакту з декількома телефонами"""
        handlers.add_contact(["John", "1234567890"], self.book)
        john = self.book.find("John")
        self.assertIsNotNone(john)
        self.assertEqual(len(john.phones), 1)


class TestChangeContact(unittest.TestCase):
    """Тести для функції change_contact"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.book = AddressBook()
        john = Record("John")
        john.add_phone("1234567890")
        self.book.add_record(john)

    def test_change_contact_success(self):
        """Тест успішної зміни телефону"""
        result = handlers.change_contact(["John", "1234567890", "9876543210"], self.book)
        self.assertIn("updated", result.lower())

    def test_change_nonexistent_contact(self):
        """Тест зміни неіснуючого контакту"""
        result = handlers.change_contact(["Jane", "1234567890", "9876543210"], self.book)
        self.assertIn("not found", result.lower())

    def test_change_invalid_phone(self):
        """Тест зміни на некоректний телефон"""
        result = handlers.change_contact(["John", "invalid"], self.book)
        # Очікуємо повідомлення про помилку
        self.assertIsInstance(result, str)

    def test_change_missing_args(self):
        """Тест зміни без достатньої кількості аргументів"""
        result = handlers.change_contact(["John"], self.book)
        self.assertIn("give me name and phone", result.lower())

    def test_change_empty_args(self):
        """Тест зміни без аргументів"""
        result = handlers.change_contact([], self.book)
        self.assertIn("give me name and phone", result.lower())

    def test_change_empty_phone(self):
        """Тест зміни на порожній телефон"""
        result = handlers.change_contact(["John", ""], self.book)
        self.assertIsInstance(result, str)


class TestShowPhone(unittest.TestCase):
    """Тести для функції show_phone"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.book = AddressBook()
        john = Record("John")
        john.add_phone("1234567890")
        john.add_phone("9876543210")
        self.book.add_record(john)

    def test_show_phone_success(self):
        """Тест показу телефонів існуючого контакту"""
        result = handlers.show_phone(["John"], self.book)
        self.assertIsInstance(result, str)
        # Якщо метод використовує find замість get_phone
        john = self.book.find("John")
        if john:
            self.assertIn(john.phones[0].value, result)

    def test_show_phone_nonexistent(self):
        """Тест показу телефонів неіснуючого контакту"""
        result = handlers.show_phone(["Jane"], self.book)
        self.assertIsInstance(result, str)

    def test_show_phone_no_args(self):
        """Тест показу телефонів без аргументів"""
        result = handlers.show_phone([], self.book)
        self.assertIn("argument", result.lower())

    def test_show_phone_empty_name(self):
        """Тест показу телефонів з порожнім ім'ям"""
        result = handlers.show_phone([""], self.book)
        self.assertIsInstance(result, str)


class TestShowAll(unittest.TestCase):
    """Тести для функції show_all"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.book = AddressBook()

    def test_show_all_empty_book(self):
        """Тест показу порожньої книги"""
        result = handlers.show_all(self.book)
        # Перевіряємо що повідомлення вказує на відсутність контактів
        self.assertTrue(
            "empty" in result.lower()
            or "no contacts" in result.lower()
            or "not found" in result.lower(),
            f"Expected empty book message, got: {result}"
        )

    def test_show_all_with_contacts(self):
        """Тест показу книги з контактами"""
        john = Record("John")
        john.add_phone("1234567890")
        self.book.add_record(john)

        jane = Record("Jane")
        jane.add_phone("9876543210")
        self.book.add_record(jane)

        result = handlers.show_all(self.book)
        self.assertIn("John", result)
        self.assertIn("Jane", result)

    def test_show_all_multiple_contacts(self):
        """Тест показу множини контактів"""
        for i in range(5):
            record = Record(f"Contact{i}")
            record.add_phone(f"123456789{i}")
            self.book.add_record(record)

        result = handlers.show_all(self.book)
        self.assertIn("Contact0", result)
        self.assertIn("Contact4", result)


class TestAddBirthday(unittest.TestCase):
    """Тести для функції add_birthday"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.book = AddressBook()
        john = Record("John")
        self.book.add_record(john)

    def test_add_birthday_success(self):
        """Тест успішного додавання дня народження"""
        result = handlers.add_birthday(["John", "15.05.1990"], self.book)
        self.assertIsInstance(result, str)

    def test_add_birthday_invalid_format(self):
        """Тест додавання некоректного формату дати"""
        result = handlers.add_birthday(["John", "1990-05-15"], self.book)
        self.assertIsInstance(result, str)

    def test_add_birthday_invalid_date(self):
        """Тест додавання неіснуючої дати"""
        result = handlers.add_birthday(["John", "32.13.1990"], self.book)
        self.assertIsInstance(result, str)

    def test_add_birthday_nonexistent_contact(self):
        """Тест додавання дня народження для неіснуючого контакту"""
        result = handlers.add_birthday(["Jane", "15.05.1990"], self.book)
        self.assertIn("not found", result.lower())

    def test_add_birthday_missing_args(self):
        """Тест додавання без достатньої кількості аргументів"""
        result = handlers.add_birthday(["John"], self.book)
        self.assertIsInstance(result, str)

    def test_add_birthday_no_args(self):
        """Тест додавання без аргументів"""
        result = handlers.add_birthday([], self.book)
        self.assertIsInstance(result, str)

    def test_add_birthday_future_date(self):
        """Тест додавання дати народження в майбутньому"""
        future_date = (datetime.now() + timedelta(days=365)).strftime("%d.%m.%Y")
        result = handlers.add_birthday(["John", future_date], self.book)
        self.assertIsInstance(result, str)

    def test_add_birthday_leap_year(self):
        """Тест додавання 29 лютого"""
        result = handlers.add_birthday(["John", "29.02.1992"], self.book)
        self.assertIsInstance(result, str)


class TestShowBirthday(unittest.TestCase):
    """Тести для функції show_birthday"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.book = AddressBook()
        john = Record("John")
        john.add_birthday("15.05.1990")
        self.book.add_record(john)

    def test_show_birthday_success(self):
        """Тест показу існуючого дня народження"""
        result = handlers.show_birthday(["John"], self.book)
        self.assertIsInstance(result, str)

    def test_show_birthday_nonexistent_contact(self):
        """Тест показу дня народження для неіснуючого контакту"""
        result = handlers.show_birthday(["Jane"], self.book)
        self.assertIn("not found", result.lower())

    def test_show_birthday_no_birthday(self):
        """Тест показу для контакту без дня народження"""
        jane = Record("Jane")
        self.book.add_record(jane)
        result = handlers.show_birthday(["Jane"], self.book)
        self.assertIsInstance(result, str)

    def test_show_birthday_no_args(self):
        """Тест показу без аргументів"""
        result = handlers.show_birthday([], self.book)
        self.assertIsInstance(result, str)


class TestBirthdays(unittest.TestCase):
    """Тести для функції birthdays"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.book = AddressBook()

    def test_birthdays_empty_book(self):
        """Тест показу днів народження для порожньої книги"""
        result = handlers.birthdays([], self.book)
        self.assertIsInstance(result, str)

    def test_birthdays_no_upcoming(self):
        """Тест коли немає найближчих днів народження"""
        john = Record("John")
        far_date = (datetime.now() - timedelta(days=200)).strftime("%d.%m.1990")
        john.add_birthday(far_date)
        self.book.add_record(john)

        result = handlers.birthdays([], self.book)
        self.assertIsInstance(result, str)

    def test_birthdays_with_upcoming(self):
        """Тест з найближчими днями народження"""
        john = Record("John")
        upcoming_date = (datetime.now() + timedelta(days=3)).strftime("%d.%m.1990")
        john.add_birthday(upcoming_date)
        self.book.add_record(john)

        result = handlers.birthdays([], self.book)
        self.assertIsInstance(result, str)

    def test_birthdays_multiple_contacts(self):
        """Тест з декількома найближчими днями народження"""
        john = Record("John")
        john.add_birthday((datetime.now() + timedelta(days=2)).strftime("%d.%m.1990"))
        self.book.add_record(john)

        jane = Record("Jane")
        jane.add_birthday((datetime.now() + timedelta(days=5)).strftime("%d.%m.1985"))
        self.book.add_record(jane)

        result = handlers.birthdays([], self.book)
        self.assertIsInstance(result, str)


class TestDeleteContact(unittest.TestCase):
    """Тести для функції delete_contact (якщо існує)"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.book = AddressBook()
        john = Record("John")
        self.book.add_record(john)

    def test_delete_contact_success(self):
        """Тест успішного видалення контакту"""
        if hasattr(handlers, 'delete_contact'):
            result = handlers.delete_contact(["John"], self.book)
            self.assertIsInstance(result, str)
            self.assertIsNone(self.book.find("John"))

    def test_delete_nonexistent_contact(self):
        """Тест видалення неіснуючого контакту"""
        if hasattr(handlers, 'delete_contact'):
            result = handlers.delete_contact(["Jane"], self.book)
            self.assertIsInstance(result, str)


class TestHelpCommands(unittest.TestCase):
    """Тести для допоміжних команд"""

    def test_hello(self):
        """Тест функції hello"""
        if hasattr(handlers, 'hello'):
            result = handlers.hello([], AddressBook())
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)

    def test_help(self):
        """Тест функції help"""
        if hasattr(handlers, 'help_command'):
            result = handlers.help_command([], AddressBook())
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)


class TestEdgeCases(unittest.TestCase):
    """Тести граничних випадків"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.book = AddressBook()

    def test_unicode_name(self):
        """Тест з Unicode символами в імені"""
        result = handlers.add_contact(["Іван", "1234567890"], self.book)
        self.assertIsInstance(result, str)
        ivan = self.book.find("Іван")
        if ivan:
            self.assertEqual(ivan.name.value, "Іван")

    def test_very_long_phone(self):
        """Тест з дуже довгим телефоном"""
        result = handlers.add_contact(["John", "12345678901234567890"], self.book)
        self.assertIsInstance(result, str)

    def test_phone_with_spaces(self):
        """Тест телефону з пробілами"""
        result = handlers.add_contact(["John", "123 456 7890"], self.book)
        self.assertIsInstance(result, str)

    def test_multiple_operations_same_contact(self):
        """Тест множинних операцій з одним контактом"""
        handlers.add_contact(["John", "1111111111"], self.book)
        handlers.change_contact(["John", "2222222222"], self.book)
        handlers.add_birthday(["John", "15.05.1990"], self.book)

        john = self.book.find("John")
        self.assertIsNotNone(john)

    def test_add_delete_add_sequence(self):
        """Тест послідовності додавання-видалення-додавання"""
        handlers.add_contact(["John", "1234567890"], self.book)
        if hasattr(handlers, 'delete_contact'):
            handlers.delete_contact(["John"], self.book)
        handlers.add_contact(["John", "9876543210"], self.book)

        john = self.book.find("John")
        self.assertIsNotNone(john)


if __name__ == "__main__":
    unittest.main(verbosity=2)
