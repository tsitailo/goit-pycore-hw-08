"""Тести для класу Field."""

import sys
import unittest
from pathlib import Path

# Додаємо батьківську директорію до sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from address_book import Field


class TestField(unittest.TestCase):
    """Тести для базового класу Field"""

    def test_field_creation(self):
        """Тест створення поля"""
        field = Field("test value")
        self.assertEqual(field.value, "test value")

    def test_field_str(self):
        """Тест конвертації поля в рядок"""
        field = Field("test")
        self.assertEqual(str(field), "test")

    def test_field_with_number(self):
        """Тест поля з числовим значенням"""
        field = Field(123)
        self.assertEqual(str(field), "123")

    def test_field_repr(self):
        """Тест представлення поля"""
        field = Field("test")
        self.assertIn("Field", repr(field))
        self.assertIn("test", repr(field))

    def test_field_with_none(self):
        """Тест поля з None"""
        field = Field(None)
        self.assertIsNone(field.value)
        self.assertEqual(str(field), "None")


if __name__ == "__main__":
    unittest.main(verbosity=2)