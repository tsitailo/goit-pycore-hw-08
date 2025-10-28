"""
Модуль для парсингу команд користувача.
"""


def parse_input(user_input):
    """
    Розбирає введений користувачем рядок на команду та аргументи.

    Args:
        user_input (str): Рядок введений користувачем

    Returns:
        tuple: Кортеж з команди (str) та списку аргументів (list)

    Examples:
        >>> parse_input("add John 123456")
        ('add', ['John', '123456'])

        >>> parse_input("  HELLO  ")
        ('hello', [])

        >>> parse_input("")
        ('', [])
    """
    user_input = user_input.strip()

    if not user_input:
        return "", []

    parts = user_input.split()
    cmd = parts[0].lower()
    args = parts[1:]

    return cmd, args
