"""Тести для класу Record."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from address_book import Record, Name


class TestRecord(unittest.TestCase):
    """Тести для класу Record"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.record = Record("John")

    def test_record_creation(self):
        """Тест створення запису"""
        self.assertIsInstance(self.record.name, Name)
        self.assertEqual(self.record.name.value, "John")
        self.assertEqual(self.record.phones, [])

    def test_add_phone(self):
        """Тест додавання телефону"""
        self.record.add_phone("1234567890")
        self.assertEqual(len(self.record.phones), 1)
        self.assertEqual(self.record.phones[0].value, "1234567890")

    def test_add_multiple_phones(self):
        """Тест додавання декількох телефонів"""
        self.record.add_phone("1234567890")
        self.record.add_phone("5555555555")
        self.assertEqual(len(self.record.phones), 2)

    def test_add_invalid_phone(self):
        """Тест додавання невалідного телефону"""
        with self.assertRaises(ValueError):
            self.record.add_phone("123")

    def test_remove_phone(self):
        """Тест видалення телефону"""
        self.record.add_phone("1234567890")
        self.record.add_phone("5555555555")
        self.record.remove_phone("1234567890")
        self.assertEqual(len(self.record.phones), 1)
        self.assertEqual(self.record.phones[0].value, "5555555555")

    def test_remove_nonexistent_phone(self):
        """Тест видалення неіснуючого телефону"""
        self.record.add_phone("1234567890")
        with self.assertRaises(ValueError) as context:
            self.record.remove_phone("9999999999")
        self.assertIn("not found", str(context.exception))

    def test_remove_phone_from_empty_list(self):
        """Тест видалення телефону з порожнього списку"""
        with self.assertRaises(ValueError):
            self.record.remove_phone("1234567890")

    def test_edit_phone(self):
        """Тест редагування телефону"""
        self.record.add_phone("1234567890")
        self.record.edit_phone("1234567890", "9876543210")
        self.assertEqual(self.record.phones[0].value, "9876543210")

    def test_edit_nonexistent_phone(self):
        """Тест редагування неіснуючого телефону"""
        self.record.add_phone("1234567890")
        with self.assertRaises(ValueError) as context:
            self.record.edit_phone("9999999999", "5555555555")
        self.assertIn("not found", str(context.exception))

    def test_edit_phone_invalid_new_number(self):
        """Тест редагування на невалідний номер"""
        self.record.add_phone("1234567890")
        with self.assertRaises(ValueError):
            self.record.edit_phone("1234567890", "123")

    def test_edit_phone_keeps_order(self):
        """Тест що редагування зберігає порядок"""
        self.record.add_phone("1111111111")
        self.record.add_phone("2222222222")
        self.record.add_phone("3333333333")
        self.record.edit_phone("2222222222", "9999999999")
        self.assertEqual(self.record.phones[0].value, "1111111111")
        self.assertEqual(self.record.phones[1].value, "9999999999")
        self.assertEqual(self.record.phones[2].value, "3333333333")

    def test_find_phone(self):
        """Тест пошуку телефону"""
        self.record.add_phone("1234567890")
        self.record.add_phone("5555555555")
        found = self.record.find_phone("5555555555")
        self.assertIsNotNone(found)
        self.assertEqual(found.value, "5555555555")

    def test_find_nonexistent_phone(self):
        """Тест пошуку неіснуючого телефону"""
        self.record.add_phone("1234567890")
        found = self.record.find_phone("9999999999")
        self.assertIsNone(found)

    def test_find_phone_empty_list(self):
        """Тест пошуку в порожньому списку"""
        found = self.record.find_phone("1234567890")
        self.assertIsNone(found)

    def test_record_str(self):
        """Тест строкового представлення запису"""
        self.record.add_phone("1234567890")
        self.record.add_phone("5555555555")
        result = str(self.record)
        self.assertIn("John", result)
        self.assertIn("1234567890", result)
        self.assertIn("5555555555", result)

    def test_record_str_no_phones(self):
        """Тест строкового представлення без телефонів"""
        result = str(self.record)
        self.assertIn("John", result)
        self.assertIn("phones:", result)

    def test_record_repr(self):
        """Тест представлення запису"""
        self.record.add_phone("1234567890")
        result = repr(self.record)
        self.assertIn("Record", result)
        self.assertIn("John", result)

    def test_remove_all_phones(self):
        """Тест видалення всіх телефонів"""
        self.record.add_phone("1111111111")
        self.record.add_phone("2222222222")
        self.record.add_phone("3333333333")

        self.record.remove_phone("1111111111")
        self.record.remove_phone("2222222222")
        self.record.remove_phone("3333333333")

        self.assertEqual(len(self.record.phones), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)