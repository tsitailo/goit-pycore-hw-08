"""Тести для класу Phone."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest  # noqa: E402

from address_book import Phone  # noqa: E402


class TestPhone(unittest.TestCase):
    """Тести для класу Phone"""

    def test_phone_valid(self):
        """Тест валідного номера телефону"""
        phone = Phone("1234567890")
        self.assertEqual(phone.value, "1234567890")

    def test_phone_invalid_length_short(self):
        """Тест короткого номера"""
        with self.assertRaises(ValueError) as context:
            Phone("123456789")
        self.assertIn("10 digits", str(context.exception))

    def test_phone_invalid_length_long(self):
        """Тест довгого номера"""
        with self.assertRaises(ValueError) as context:
            Phone("12345678901")
        self.assertIn("10 digits", str(context.exception))

    def test_phone_with_letters(self):
        """Тест номера з літерами"""
        with self.assertRaises(ValueError):
            Phone("123abc7890")

    def test_phone_with_special_chars(self):
        """Тест номера зі спеціальними символами"""
        with self.assertRaises(ValueError):
            Phone("123-456-7890")

    def test_phone_with_spaces(self):
        """Тест номера з пробілами"""
        with self.assertRaises(ValueError):
            Phone("123 456 7890")

    def test_phone_empty(self):
        """Тест порожнього номера"""
        with self.assertRaises(ValueError):
            Phone("")

    def test_phone_with_plus(self):
        """Тест номера з символом +"""
        with self.assertRaises(ValueError):
            Phone("+1234567890")

    def test_phone_validate_method(self):
        """Тест методу валідації"""
        self.assertTrue(Phone.validate("9876543210"))
        self.assertFalse(Phone.validate("123"))
        self.assertFalse(Phone.validate("abcdefghij"))
        self.assertFalse(Phone.validate("123-456-7890"))

    def test_phone_with_parentheses(self):
        """Тест номера з дужками"""
        with self.assertRaises(ValueError):
            Phone("(123)456789")

    def test_phone_with_dots(self):
        """Тест номера з крапками"""
        with self.assertRaises(ValueError):
            Phone("123.456.7890")

    def test_phone_none(self):
        """Тест з None"""
        with self.assertRaises(ValueError):
            Phone(None)

    def test_phone_all_zeros(self):
        """Тест номера з усіма нулями"""
        phone = Phone("0000000000")
        self.assertEqual(phone.value, "0000000000")

    def test_phone_all_nines(self):
        """Тест номера з усіма дев'ятками"""
        phone = Phone("9999999999")
        self.assertEqual(phone.value, "9999999999")


if __name__ == "__main__":
    unittest.main(verbosity=2)
