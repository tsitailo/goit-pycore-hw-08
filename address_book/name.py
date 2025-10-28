"""Клас для зберігання імені контакту."""

from .field import Field


class Name(Field):
    """
    Клас для зберігання імені контакту.

    Обов'язкове поле з валідацією на порожнє значення.

    Attributes:
        value: Ім'я контакту

    Raises:
        ValueError: Якщо ім'я порожнє або None
    """

    def __init__(self, value):
        """
        Ініціалізація імені з валідацією.

        Args:
            value: Ім'я контакту

        Raises:
            ValueError: Якщо ім'я порожнє або None
        """
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)
