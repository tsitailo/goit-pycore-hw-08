"""Тести для класу Name."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from address_book import Name


class TestName(unittest.TestCase):
    """Тести для класу Name"""

    def test_name_creation(self):
        """Тест створення імені"""
        name = Name("John")
        self.assertEqual(name.value, "John")

    def test_name_empty_string(self):
        """Тест створення імені з порожнім рядком"""
        with self.assertRaises(ValueError) as context:
            Name("")
        self.assertIn("Name cannot be empty", str(context.exception))

    def test_name_none(self):
        """Тест створення імені з None"""
        with self.assertRaises(ValueError):
            Name(None)

    def test_name_with_spaces(self):
        """Тест створення імені з пробілами"""
        name = Name("John Doe")
        self.assertEqual(name.value, "John Doe")

    def test_name_str(self):
        """Тест конвертації імені в рядок"""
        name = Name("Alice")
        self.assertEqual(str(name), "Alice")

    def test_name_with_special_chars(self):
        """Тест імені зі спеціальними символами"""
        name = Name("O'Brien")
        self.assertEqual(name.value, "O'Brien")

    def test_name_with_numbers(self):
        """Тест імені з цифрами"""
        name = Name("John123")
        self.assertEqual(name.value, "John123")

    def test_name_unicode(self):
        """Тест імені з Unicode символами"""
        name = Name("Олександр")
        self.assertEqual(name.value, "Олександр")


if __name__ == "__main__":
    unittest.main(verbosity=2)