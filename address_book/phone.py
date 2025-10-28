"""Клас для зберігання номера телефону."""

from .field import Field


class Phone(Field):
    """
    Клас для зберігання номера телефону.

    Має валідацію формату - номер повинен містити рівно 10 цифр.

    Attributes:
        value: Номер телефону

    Raises:
        ValueError: Якщо номер не відповідає формату (10 цифр)
    """

    def __init__(self, value):
        """
        Ініціалізація телефону з валідацією.

        Args:
            value: Номер телефону (10 цифр)

        Raises:
            ValueError: Якщо номер не містить рівно 10 цифр
        """
        if not self.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

    @staticmethod
    def validate(value):
        """
        Валідація номера телефону.

        Args:
            value: Номер для перевірки

        Returns:
            bool: True якщо номер валідний, False інакше
        """
        return isinstance(value, str) and value.isdigit() and len(value) == 10
