"""Базовий клас для полів запису."""


class Field:
    """
    Базовий клас для полів запису.

    Attributes:
        value: Значення поля
    """

    def __init__(self, value):
        """
        Ініціалізація поля.

        Args:
            value: Значення поля
        """
        self.value = value

    def __str__(self):
        """
        Повертає строкове представлення поля.

        Returns:
            str: Значення поля як рядок
        """
        return str(self.value)

    def __repr__(self):
        """
        Повертає представлення об'єкта для розробників.

        Returns:
            str: Представлення об'єкта
        """
        return f"{self.__class__.__name__}(value={self.value!r})"
